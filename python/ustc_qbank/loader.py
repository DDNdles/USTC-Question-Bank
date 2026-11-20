"""Core loader and query interface for USTC-Question-Bank."""

from __future__ import annotations

import json
import pathlib
import random
from dataclasses import dataclass
from typing import Any, Iterable, Iterator


def _default_repo_root() -> pathlib.Path:
    """Locate repository root containing manifest.json."""
    candidate = pathlib.Path(__file__).resolve().parents[2]
    if (candidate / "manifest.json").is_file():
        return candidate
    cwd = pathlib.Path.cwd().resolve()
    for base in (cwd, *cwd.parents):
        if (base / "manifest.json").is_file() and (base / "courses").is_dir():
            return base
    raise FileNotFoundError(
        "Could not locate manifest.json. Pass root='/path/to/USTC-Question-Bank' explicitly."
    )


@dataclass(frozen=True)
class TaxonomyNode:
    id: str
    parent_id: str | None
    level: int
    name: str
    chapter_ref: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TaxonomyNode:
        return cls(
            id=data["id"],
            parent_id=data.get("parent_id"),
            level=int(data["level"]),
            name=data["name"],
            chapter_ref=data.get("chapter_ref"),
        )


@dataclass(frozen=True)
class FigureRef:
    id: str
    path: str
    alt: str
    caption: str | None = None
    width: int | None = None
    height: int | None = None
    sha256: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FigureRef:
        return cls(
            id=data["id"],
            path=data["path"],
            alt=data["alt"],
            caption=data.get("caption"),
            width=data.get("width"),
            height=data.get("height"),
            sha256=data.get("sha256"),
        )


@dataclass(frozen=True)
class QuestionOption:
    key: str
    md: str
    figures: tuple[FigureRef, ...] = ()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> QuestionOption:
        return cls(
            key=data["key"],
            md=data["md"],
            figures=tuple(FigureRef.from_dict(f) for f in (data.get("figures") or ())),
        )


@dataclass(frozen=True)
class Question:
    id: str
    course_code: str
    schema_version: str
    type: str
    stem_md: str
    stem_figures: tuple[FigureRef, ...]
    options: tuple[QuestionOption, ...]
    answer_md: str
    answer_figures: tuple[FigureRef, ...]
    answer_origin: str
    answer_origin_detail: str
    solution_md: str
    solution_steps: tuple[str, ...]
    solution_figures: tuple[FigureRef, ...]
    kp_ids: tuple[str, ...]
    keywords: tuple[str, ...]
    difficulty: int
    source_kind: str
    source_batch: str
    source_ref: str
    source_year: int | None
    source_term: str | None
    source_exam_kind: str | None
    source_url: str | None
    source_rights: str
    quarantined: bool
    quarantine_reason: str | None
    confidence: float | None
    note: str | None
    overlap_hint: str | None
    raw: dict[str, Any]

    @property
    def has_figures(self) -> bool:
        return bool(
            self.stem_figures
            or self.answer_figures
            or self.solution_figures
            or any(opt.figures for opt in self.options)
        )

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Question:
        return cls(
            id=d["id"],
            course_code=d["course_code"],
            schema_version=d["schema_version"],
            type=d["type"],
            stem_md=d["stem"]["md"],
            stem_figures=tuple(FigureRef.from_dict(f) for f in (d["stem"].get("figures") or ())),
            options=tuple(QuestionOption.from_dict(o) for o in (d.get("options") or ())),
            answer_md=d["answer"]["md"],
            answer_figures=tuple(FigureRef.from_dict(f) for f in (d["answer"].get("figures") or ())),
            answer_origin=d["answer"]["origin"],
            answer_origin_detail=d["answer"]["origin_detail"],
            solution_md=d["solution"]["md"],
            solution_steps=tuple(d["solution"].get("steps") or ()),
            solution_figures=tuple(FigureRef.from_dict(f) for f in (d["solution"].get("figures") or ())),
            kp_ids=tuple(d["tags"]["kp_ids"]),
            keywords=tuple(d["tags"].get("keywords") or ()),
            difficulty=int(d["tags"]["difficulty"]),
            source_kind=d["source"]["kind"],
            source_batch=d["source"]["batch"],
            source_ref=d["source"]["ref"],
            source_year=d["source"].get("year"),
            source_term=d["source"].get("term"),
            source_exam_kind=d["source"].get("exam_kind"),
            source_url=d["source"].get("url"),
            source_rights=d["source"]["rights"],
            quarantined=bool(d["quality"]["quarantined"]),
            quarantine_reason=d["quality"].get("quarantine_reason"),
            confidence=d["quality"].get("confidence"),
            note=d["quality"].get("note"),
            overlap_hint=d["quality"].get("overlap_hint"),
            raw=d,
        )

    def to_dict(self) -> dict[str, Any]:
        return self.raw


class Course:
    """Single USTC course question bank with taxonomy-aware querying."""

    def __init__(self, root: pathlib.Path, code: str, *, asset_base_url: str | None = None) -> None:
        self.root = root
        self.code = code
        self.asset_base_url = asset_base_url
        self.dir = root / "courses" / code
        if not self.dir.is_dir():
            raise KeyError(f"Course directory not found: {self.dir}")

        self.meta: dict[str, Any] = json.loads((self.dir / "meta.json").read_text(encoding="utf-8"))
        tax_data = json.loads((self.dir / "taxonomy.json").read_text(encoding="utf-8"))
        self.taxonomy: list[TaxonomyNode] = [TaxonomyNode.from_dict(n) for n in tax_data["nodes"]]
        self._children: dict[str | None, list[str]] = {}
        self._node_map: dict[str, TaxonomyNode] = {}
        for node in self.taxonomy:
            self._node_map[node.id] = node
            self._children.setdefault(node.parent_id, []).append(node.id)
        self._questions: list[Question] | None = None

    @property
    def name(self) -> str:
        return self.meta["name"]

    def resolve_asset(self, figure_path: str) -> str:
        """Resolve a course-relative figure path to a remote URL (if configured) or local path."""
        clean = figure_path.lstrip("/")
        if self.asset_base_url:
            base = self.asset_base_url.rstrip("/")
            return f"{base}/courses/{self.code}/{clean}"
        return str((self.dir / clean).resolve())

    def questions(self) -> list[Question]:
        if self._questions is None:
            path = self.dir / "questions.jsonl"
            items: list[Question] = []
            with path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        items.append(Question.from_dict(json.loads(line)))
            self._questions = items
        return self._questions

    def __len__(self) -> int:
        return len(self.questions())

    def __iter__(self) -> Iterator[Question]:
        return iter(self.questions())

    def expand_kp(self, kp_id: str) -> set[str]:
        """Return kp_id and all descendant knowledge point IDs in the taxonomy tree."""
        result: set[str] = set()
        stack = [kp_id]
        while stack:
            curr = stack.pop()
            if curr in result:
                continue
            result.add(curr)
            stack.extend(self._children.get(curr, ()))
        return result

    def query(
        self,
        *,
        kp: str | Iterable[str] | None = None,
        origins: Iterable[str] | None = None,
        batches: Iterable[str] | None = None,
        exclude_batches: Iterable[str] | None = None,
        source_kinds: Iterable[str] | None = None,
        exam_kinds: Iterable[str] | None = None,
        years: Iterable[int] | None = None,
        difficulty: tuple[int, int] | None = None,
        qtypes: Iterable[str] | None = None,
        has_figures: bool | None = None,
        exclude_quarantined: bool = True,
        text: str | None = None,
    ) -> list[Question]:
        kp_set: set[str] | None = None
        if kp is not None:
            raw_kps = [kp] if isinstance(kp, str) else list(kp)
            kp_set = set()
            for k in raw_kps:
                kp_set.update(self.expand_kp(k))

        origin_set = set(origins) if origins is not None else None
        batch_set = set(batches) if batches is not None else None
        excl_batch_set = set(exclude_batches) if exclude_batches is not None else None
        kind_set = set(source_kinds) if source_kinds is not None else None
        exam_set = set(exam_kinds) if exam_kinds is not None else None
        year_set = set(years) if years is not None else None
        qtype_set = set(qtypes) if qtypes is not None else None
        needle = text.lower() if text else None

        out: list[Question] = []
        for q in self.questions():
            if exclude_quarantined and q.quarantined:
                continue
            if has_figures is not None and q.has_figures != has_figures:
                continue
            if kp_set is not None and not (kp_set.intersection(q.kp_ids)):
                continue
            if origin_set is not None and q.answer_origin not in origin_set:
                continue
            if batch_set is not None and q.source_batch not in batch_set:
                continue
            if excl_batch_set is not None and q.source_batch in excl_batch_set:
                continue
            if kind_set is not None and q.source_kind not in kind_set:
                continue
            if exam_set is not None and q.source_exam_kind not in exam_set:
                continue
            if year_set is not None and q.source_year not in year_set:
                continue
            if difficulty is not None and not (difficulty[0] <= q.difficulty <= difficulty[1]):
                continue
            if qtype_set is not None and q.type not in qtype_set:
                continue
            if needle is not None:
                haystack = f"{q.stem_md}\n{q.answer_md}\n{q.source_ref}\n{' '.join(q.keywords)}".lower()
                if needle not in haystack:
                    continue
            out.append(q)
        return out

    def sample(
        self,
        n: int,
        *,
        seed: int | None = None,
        **query_kwargs: Any,
    ) -> list[Question]:
        pool = self.query(**query_kwargs)
        rng = random.Random(seed)
        if n >= len(pool):
            result = list(pool)
            rng.shuffle(result)
            return result
        return rng.sample(pool, n)


class QuestionBank:
    """Top-level entry point for loading all courses in USTC-Question-Bank."""

    def __init__(self, root: str | pathlib.Path | None = None) -> None:
        self.root = pathlib.Path(root).resolve() if root is not None else _default_repo_root()
        manifest_path = self.root / "manifest.json"
        if not manifest_path.is_file():
            raise FileNotFoundError(f"manifest.json not found under {self.root}")
        self.manifest: dict[str, Any] = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.asset_base_url: str | None = self.manifest.get("asset_base_url")
        self._courses: dict[str, Course] = {}

    @property
    def course_codes(self) -> list[str]:
        return [c["code"] for c in self.manifest["courses"]]

    def course(self, code: str) -> Course:
        if code not in self._courses:
            self._courses[code] = Course(self.root, code, asset_base_url=self.asset_base_url)
        return self._courses[code]

    def __getitem__(self, code: str) -> Course:
        return self.course(code)

    def all_questions(self, *, exclude_quarantined: bool = False) -> list[Question]:
        out: list[Question] = []
        for code in self.course_codes:
            out.extend(self.course(code).query(exclude_quarantined=exclude_quarantined))
        return out

    def get(self, question_id: str) -> Question:
        code = question_id.split("-", 1)[0]
        if code in self.course_codes:
            for q in self.course(code).questions():
                if q.id == question_id:
                    return q
        for c in self.course_codes:
            for q in self.course(c).questions():
                if q.id == question_id:
                    return q
        raise KeyError(f"Question not found: {question_id}")
