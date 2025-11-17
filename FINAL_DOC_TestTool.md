## FINAL_DOC: TestTool 프로젝트

### 1) 프로젝트 룰(抜粋)
- **목적**: PTZ 카메라 제어·테스트를 단일 GUI에서 효율화/자동화
- **우선순위**: 안정성 > 성능 > 호환성 > 사용성 > 확장성
- **제약**: 기존 프로토콜 호환, 4채널 동시 스트리밍 실시간성, UI 블로킹 금지, 확장 용이성
- **범위**: Python GUI(Tkinter 중심), RTSP 표시, PTZ 제어, 로그 관리(클라우드/외부 API 제외)

### 2) 요구사항 저지(요건適合 판단)
- 안정성: 예외/네트워크 오류 처리(Communication.py), 디바운스(KeyBind.py)로 충족
- 성능: 소켓 재사용/멀티스레드 사용, 4채널 동시 처리 대상. 추가 프로파일링 필요
- 호환성: Uncooled/DRS/FineTree/NYX/MiniGimbal/Multi/PT Driver 분기 구현됨
- 사용성: 키보드 바인딩/PTZ UI/로그 표시/시스템 정보 탭 제공
- 확장성: 모델 분기/상수 중앙집중(Cons) 구조로 확장 용이

### 3) 변경 대상(파일/함수)
- 파일
  - `KeyBind.py`: 키 입력 처리, 모델 분기, 디바운스, stop 처리
  - `Ptz.py`: PTZ 버튼 UI, 모델별 전송 래퍼
  - `Communication.py`: 모델별 통신(소켓/TCP/HTTP Digest), 응답 파싱/로그
  - `UI_Init.py`, `Response.py`, `System_Info.py`, `Table.py`: UI/로그/시스템 정보/명령 테이블
- 함수(例)
  - `KeyBind.handle_ptz_move`, `KeyBind.handle_ptz_stop`, `KeyBind.initialize_ptz`
  - `Ptz.PTZ.send_miniGimbal`, `Ptz.PTZ.send_pt_drv`
  - `Communication.send_cmd_for_uncooled`, `send_cmd_for_uncooled_only_cmd`, `send_cmd_for_drs`, `fine_tree_send_cgi`, `send_cmd_to_Finetree`, `send_cmd_to_nyx(_without_root)`, `send_cmd_to_nyx_with_interval`

### 4) 데이터 설계 방침
- 설정/상태는 `Constant.py`에 단일 소스 유지: 채널 정보(`selected_ch`), 모델(`selected_model`), 버퍼/포트, 로그 버퍼 등
- 응답 데이터는 모델별 Dict로 구조화 저장(예: `uncooled_*_q`, `drs_response`, `miniG_res_payload`)
- 로그는 텍스트/엑셀 혼합 저장(미니짐벌 응답 텍스트·xlsx 양식 지원)
- 스레드/소켓 공유 시 최소 공유 상태만 유지하고 접근은 함수 경유로 일원화

### 5) 화면 설계 방침
- 메인: 명령 테이블(Treeview), 로그 창, 시스템 정보 패널, PTZ 조이스틱 영역
- 조작: 키보드 바인딩(방향, Prior/Next/Insert/Delete/End 등), 버튼 기반 PTZ 조작
- 피드백: 상태/로그 실시간 반영, 응답 전문 일부 축약 표시, 중요 상태는 토스트/다이얼로그
- 4채널 확장: 플레이어 컨테이너 기준 레이아웃(비동기 업데이트, 프레임 드롭 감시)

### 6) 처리 플로우
```mermaid
graph TD
    A[사용자 입력] --> B{입력 타입}
    B -->|키보드| C[KeyBind.py]
    B -->|GUI 버튼| D[Ptz.py]
    B -->|테이블 선택| E[Table.py]

    C --> F[모델 분기]
    D --> F
    E --> F

    F -->|Uncooled| G[헥스 전송]
    F -->|DRS| H[소켓/바이너리]
    F -->|FineTree| I[HTTP Digest]
    F -->|NYX| J[소켓/문자 프로토콜]
    F -->|MiniGimbal| K[바이너리]
    F -->|Multi/PT Driver| L[TCP 제어]

    G --> M[Communication.py]
    H --> M
    I --> M
    J --> M
    K --> M
    L --> M

    M --> N[응답 파싱/저장]
    N --> O[로그 출력(Response.py)]
    N --> P[UI 업데이트]
    N --> Q[시스템 정보 갱신]
```

### 7) 개발 공수 견적
- PTZ 통합/검증: 40h
- 멀티스레딩 안정화: 32h
- RTSP 최적화: 24h
- 로그 시스템 고도화: 16h
- UI/UX 개선: 20h
- 테스트/디버깅: 24h
- 문서화: 8h
- 합계: 164h ≒ 20.5 인일(1인 기준 8h/일)

### 8) 미확정 사항 & TODO
- 긴급 확인
  - [ ] 모델별 최신 프로토콜/펌웨어 차이 정리
  - [ ] 4채널 동시 스트리밍 지연 허용 기준(ms)
  - [ ] 사내/현장 네트워크 보안 제한 목록
- 중요 확인
  - [ ] 권한 분리 필요 여부(관리자/사용자)
  - [ ] 로그/설정 백업 주기 및 보존 정책
  - [ ] Windows 10/11 빌드별 호환성 범위
- 일반 확인
  - [ ] 배포 형태(설치형/포터블) 결정
  - [ ] 다국어 범위(ko/en/ja) 확정
  - [ ] 업데이트 정책(자동/수동)


