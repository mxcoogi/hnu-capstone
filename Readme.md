
---

## API 명세서

| **엔드포인트**   | **HTTP 메서드** | **설명**                          | **요청**                              | **응답 코드**     | **성공 응답**                                                                                       | **에러 응답**                                        |
|------------------|-----------------|-----------------------------------|---------------------------------------|-------------------|----------------------------------------------------------------------------------------------------|------------------------------------------------------|
| `/ping`          | `GET`           | 서버 상태 확인용 API             | `GET /ping`                           | `200 OK`          | `{ "message": "pong" }`                                                                           | -                                                    |
| `/sign-up`      | `POST`          | 회원가입 API                     | `{ "student_id": "string", "name": "string", "password": "string" }` | `201 Created`     | `{ "message": "User registered successfully.", "user_id": "string" }`                             | `400 Bad Request`: `{ "error": "Invalid input data." }`<br>`409 Conflict`: `{ "error": "Student ID already exists." }` |
| `/login`         | `POST`          | 로그인 API                       | `{ "student_id": "string", "password": "string" }`                 | `200 OK`          | `{ "message": "Login successful.", "token": "string" }`                                         | `401 Unauthorized`: `{ "error": "Invalid student ID or password." }` |
| `/mypage`        | `GET`           | 마이페이지 조회 API             | `GET /mypage`                        | `200 OK`          | `{ "average_grade": "number", "department": "string", "volunteer_hours": "number" }`            | -                                                    |
| `/mypage`        | `POST`          | 마이페이지 정보 수정 API       | `{ "average_grade": "float", "department": "string", "volunteer_hours": "float" }` | `200 OK`          | `{ "message": "Mypage information updated successfully." }`                                      | `400 Bad Request`: `{ "error": "Invalid input data." }` |
| `/chat-api`      | `POST`          | 챗봇 요청 API                   | `{ "token": "string", "request_message": "string" }`               | `200 OK`          | `{ "response_message": "string" }`                                                               | `400 Bad Request`: `{ "error": "Invalid input data." }` |

---