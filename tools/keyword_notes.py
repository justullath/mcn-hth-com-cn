from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

SAMPLE_URL = "https://mcn-hth.com.cn"
SAMPLE_KEYWORD = "华体会"

@dataclass
class KeywordNote:
    keyword: str
    url: str
    note: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def summary(self) -> str:
        tags_str = ", ".join(self.tags) if self.tags else "无标签"
        return f"[{self.keyword}] ({self.url}) 标签: {tags_str}"

    def formatted_output(self, include_time: bool = False) -> str:
        base = f"关键词: {self.keyword}\n链接: {self.url}\n备注: {self.note}\n标签: {', '.join(self.tags) if self.tags else '无'}"
        if include_time:
            base += f"\n创建时间: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        return base

@dataclass
class NoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [note for note in self.notes if note.keyword == keyword]

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [note for note in self.notes if tag in note.tags]

    def list_all(self) -> None:
        for i, note in enumerate(self.notes, 1):
            print(f"{i}. {note.summary()}")

    def export_all(self, include_time: bool = False) -> List[str]:
        return [note.formatted_output(include_time) for note in self.notes]

def format_note_list(notes: List[KeywordNote], title: str = "笔记列表") -> str:
    lines = [f"=== {title} ==="]
    for idx, note in enumerate(notes, 1):
        lines.append(f"{idx}. {note.summary()}")
    return "\n".join(lines)

def build_sample_collection() -> NoteCollection:
    collection = NoteCollection()
    note1 = KeywordNote(
        keyword=SAMPLE_KEYWORD,
        url=SAMPLE_URL,
        note="这是一个示例关键词笔记",
        tags=["示例", "关键词"],
    )
    note2 = KeywordNote(
        keyword="体育新闻",
        url="https://example.com/sports",
        note="体育相关的内容聚合",
        tags=["体育", "新闻"],
    )
    note3 = KeywordNote(
        keyword="华体会",
        url="https://mcn-hth.com.cn/about",
        note="关于华体会的更多介绍",
        tags=["华体会", "介绍"],
    )
    collection.add_note(note1)
    collection.add_note(note2)
    collection.add_note(note3)
    return collection

def main():
    print("=== 关键词笔记系统演示 ===")
    print(f"示例URL: {SAMPLE_URL}")
    print(f"示例关键词: {SAMPLE_KEYWORD}")
    print()

    collection = build_sample_collection()
    print("所有笔记:")
    collection.list_all()
    print()

    keyword_to_find = "华体会"
    found = collection.find_by_keyword(keyword_to_find)
    if found:
        print(f"找到关键词 '{keyword_to_find}' 的笔记:")
        for note in found:
            print(note.formatted_output(include_time=True))
            print()

    tag_to_find = "示例"
    tagged_notes = collection.find_by_tag(tag_to_find)
    print(f"标签 '{tag_to_find}' 的笔记:")
    for note in tagged_notes:
        print(note.formatted_output())
        print()

    print("导出全部笔记:")
    exported = collection.export_all(include_time=True)
    for item in exported:
        print(item)
        print("---")

    print("格式化列表:")
    print(format_note_list(collection.notes, "全部笔记"))

if __name__ == "__main__":
    main()