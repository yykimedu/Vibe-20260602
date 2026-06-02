# Tetris (Pygame 포팅)

HTML/JS 구현을 Pygame으로 포팅한 단일 파일 버전입니다.

필수 패키지 설치:

```bash
python -m pip install -r requirements.txt
```

실행:

```bash
python tetris.py
```

조작:

- ← → : 좌/우 이동
- ↑ : 회전
- ↓ : 소프트 드롭
- Space : 하드 드롭
- P : 일시정지

파일:

- [tetris.py](tetris.py) — 메인 게임 파일
- [tetris.html](tetris.html) — 원본 HTML/JS 구현 (참조)

주의:

- GUI 환경에서 실행하세요 (서버의 헤드리스 환경에서는 동작하지 않을 수 있습니다).
- Pygame 버전이 다르면 동작 방식이 다를 수 있습니다.
