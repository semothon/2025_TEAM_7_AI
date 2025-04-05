class User:
    def __init__(self, username, realName, university, department, studentId, grade):
        self.username: str = username
        self.realName: str = realName
        self.university: str = university
        self.department: str = department
        self.studentId: int = studentId
        self.grade: int = grade

class Party:
    def __init__(self, id, name, description, category, subCategory, targetMember, maximumMember, hashtags, thumbnailUrl, memberCount, whereMeet, whenMeet, howApply):
        self.id: int = id
        self.name: str = name
        self.description: str | None = description
        self.category: str = category
        self.subCategory: str = subCategory
        self.targetMember: str = targetMember
        self.maximumMember: int = maximumMember
        self.hashtags: list[str] = hashtags
        self.thumbnailUrl: str | None = thumbnailUrl
        self.memberCount: int = memberCount
        self.whereMeet: str | None = whereMeet
        self.whenMeet: str | None = whenMeet
        self.howApply: str | None = howApply

class RecommendRequest:
    def __init__(self, content: str, parties: list[Party], user: User):
        self.content: str = content  # ✅ 사용자가 원하는 모임에 대한 설명
        self.parties: list[Party] = parties
        self.user: User = user  # ✅ 사용자 정보도 함께 받음