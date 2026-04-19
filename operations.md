# KOR MEET Operations Log

## 프로젝트 정보
- **브랜드**: KOR MEET (구 KORCALL)
- **콘셉트**: ENGCALL 모델 플립 — 한국인 원어민 튜터가 외국인에게 한국어 1:1 화상수업
- **전략**: 프리미엄 (한국인 튜터 인건비 고려)
- **라이브 URL**: https://tjaypark.github.io/korcall-landing/
- **레포**: https://github.com/TJayPark/korcall-landing

## 로컬 프리뷰
- 프로젝트 루트에서 `python3 -m http.server 18091` 실행
- 브라우저에서 `http://127.0.0.1:18091/` 접속
- 종료 방법과 추가 메모는 `README.md` 참고

---

## 타겟 시장
| 국가 | 도시 | 이유 | 채널 |
|------|------|------|------|
| 🇹🇭 태국 | 방콕 | K-pop 팬 규모 1위, 빈부격차 큼 | LINE, TikTok, Instagram |
| 🇭🇰 홍콩 | - | 높은 구매력, 교육열 | 小红书, Instagram, Facebook |
| 🇮🇩 인도네시아 | 자카르타 | 인구 대국 + 부유층 존재 | WhatsApp, TikTok, Instagram |

---

## 완료된 작업

### 2026-04-13 ~ 04-15: 시장 조사 + 랜딩페이지 구축

#### 시장 조사
- [x] 타겟 국가 선정 (6개국 → 프리미엄 전략으로 피벗 → 3개국 확정)
- [x] 국가별 한류 열기 × 빈부격차 × 부자도시 교육열 프레임워크 스코어링
- [x] 시장 조사 리포트 작성 (~/tjay_marketing/output/korcall/market-research-2026.md)

#### 랜딩페이지
- [x] 단독 HTML 랜딩페이지 구축 (index.html, 빌드 도구 없음)
- [x] GitHub Pages 배포 + CNAME 설정
- [x] ENGCALL 브랜딩 적용 (sage green #7d8f74, golden #ffbc3b, cream #f7f3ed, navy #182b45)
- [x] 언어 스위처 구현 (EN/TH/ID, URL ?lang= 파라미터 + localStorage)
- [x] 91개 data-i18n 속성 + 3개 언어 번역 객체
- [x] 사전등록 폼 (Formspree + Google Forms 이중 제출)
- [x] UTM 파라미터 추적 (hidden fields)
- [x] GA4 커스텀 이벤트 설정 (waitlist_signup, language_switch)

#### 카피라이팅
- [x] 파운더 스토리 섹션 추가
- [x] **자청 초사고 글쓰기 프레임워크 적용 리라이트** (2026-04-15)
  - 마인드리딩 훅: "넌 이미 한국어 알아 — 근데 막상 말하면 안 나오지?"
  - Yes Set: Duolingo → YouTube → 먼지 쌓인 교재 (3연속 동의)
  - 스토리텔링 갈등: 동남아 여행 → K-팬의 한국어 배울 곳 없는 현실 목격
  - 스토리텔링 해소: 8년 ENGCALL 운영 경험 → 같은 시스템 뒤집기
  - 반박제거: "사기 아닌가?" → 실제 회사 + 100% 환불 보장
  - 행동유발: "네 튜터는 준비됐다. 넌 준비됐어?"
- [x] Trust Cards 카피 강화 (3개)

#### 마케팅 자산
- [x] 광고 카피 9개 (국가별 3개: ad-copy.md)
- [x] TikTok/Reels 스크립트 5개 (video-scripts.md)
- [x] K-팬 커뮤니티 리스트 (community-list.md)
- [x] 설문 23문항 (survey-questions.md)
- [x] 프로모 영상 3개 (Python moviepy 자동 생성)

---

## 미완료 작업

### 즉시 (배포 전)
- [ ] Formspree endpoint 교체 (`YOUR_FORM_ID` → 실제 ID)
- [ ] Google Forms URL 교체 (플레이스홀더 → 실제 URL)
- [ ] GA4 measurement ID 교체 (`G-XXXXXXXXXX` → 실제 ID)

### 수요 검증 (Plan A)
- [ ] Google Forms 설문 생성 (survey-questions.md 기반)
- [ ] Formspree 계정 생성 + endpoint 발급
- [ ] GA4 속성 생성 + measurement ID 발급
- [ ] 국가별 소액 광고 집행 ($50-100/국가, 총 $150-300)
  - 태국: Instagram/TikTok → ?lang=th&utm_source=...
  - 홍콩: Instagram/Facebook → ?lang=en&utm_source=...
  - 인도네시아: TikTok/Instagram → ?lang=id&utm_source=...
- [ ] 2주간 데이터 수집
- [ ] 결과 분석: 국가별 대기자 등록 수, 전환율, CPC 비교

### 이후 (검증 성공 시)
- [ ] MVP 개발 (ENGCALL 인프라 재활용)
- [ ] 튜터 모집 (한국인 원어민)
- [ ] 가격 책정 (프리미엄 전략)
- [ ] 결제 시스템 연동

---

## Git 커밋 로그
| 해시 | 날짜 | 내용 |
|------|------|------|
| 75cb543 | 2026-04-14 | Initial commit (KORCALL 브랜딩) |
| df076a8 | 2026-04-14 | Rebrand KORCALL → KOR MEET + ENGCALL 색상 |
| cac824a | 2026-04-15 | 파운더 스토리 + 언어 스위처 추가 |
| c1a28c1 | 2026-04-15 | 초사고 글쓰기 프레임워크 파운더 스토리 리라이트 |

---

## 기술 스택
- **프론트**: 단독 HTML + CSS Custom Properties + Vanilla JS
- **배포**: GitHub Pages (master branch)
- **폼**: Formspree (primary) + Google Forms (fallback)
- **분석**: GA4 + UTM 파라미터
- **영상**: Python moviepy (1080x1920 TikTok/Reels 포맷)
- **i18n**: data-i18n attribute + JS translations object + URL ?lang= parameter
