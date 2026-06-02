from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Developer:
    name: str
    role: str
    main_language: str
    joined_year: int
    skills: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        current_year = date.today().year

        if not self.name.strip():
            raise ValueError("name은 비어 있을 수 없습니다.")

        if self.joined_year > current_year:
            raise ValueError("joined_year는 현재 연도보다 클 수 없습니다.")

    @property
    def years_of_experience(self) -> int:
        """입사 연도를 기준으로 경력 연수를 계산합니다."""
        return date.today().year - self.joined_year

    def add_skill(self, skill: str) -> None:
        """개발자의 기술 스택을 추가합니다."""
        skill = skill.strip()

        if not skill:
            raise ValueError("skill은 비어 있을 수 없습니다.")

        if skill not in self.skills:
            self.skills.append(skill)

    def introduce(self) -> str:
        """개발자 소개 문장을 반환합니다."""
        skill_text = ", ".join(self.skills) if self.skills else "등록된 기술 없음"

        return (
            f"안녕하세요. 저는 {self.name}입니다. "
            f"역할은 {self.role}이고, 주 사용 언어는 {self.main_language}입니다. "
            f"경력은 {self.years_of_experience}년이며, "
            f"보유 기술은 {skill_text}입니다."
        )