---
type: moc
aliases:
  - <% tp.file.title %>
description: ""
author:
  - Claude
model: 
effort: 
date created: <% tp.date.now("YYYY-MM-DDTHH:mm") %>
date modified: <% tp.date.now("YYYY-MM-DDTHH:mm") %>
tags:
  - moc
topic: []
related: []
status: active
---

# <% tp.file.title %>

> 이 Map of Content는 관련 Wiki 페이지들을 주제별로 묶어 탐색을 돕습니다.

---

## Core Pages



---

## Related Topics



---

## Recently Updated

*Dataview query로 자동 갱신:*

```dataview
TABLE date modified as "Modified", confidence as "Confidence"
FROM "20. Wiki"
WHERE contains(tags, this.topic)
SORT date modified DESC
LIMIT 10
```
