from pydantic import BaseModel

class User(BaseModel):
    username: str
    realName: str
    university: str
    department: str
    studentId: str
    grade: str

class Party(BaseModel):
    id: int
    name: str
    description: str | None
    category: str
    subCategory: str
    targetMember: str
    maximumMember: int
    hashtags: list[str]
    thumbnailUrl: str | None
    memberCount: int
    whereMeet: str | None
    whenMeet: str | None
    howApply: str | None

class RecommendRequest(BaseModel):
    content: str
    parties: list[Party]
    user: User  # ✅ 사용자 정보도 함께 받음