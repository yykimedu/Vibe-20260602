// ============================================
// MOBILE MENU TOGGLE
// ============================================

const hamburger = document.getElementById('hamburger');
const navMenu = document.querySelector('.nav-menu');

if (hamburger) {
    hamburger.addEventListener('click', function() {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });
}

// 메뉴 항목 클릭 시 메뉴 닫기
if (navMenu) {
    const navLinks = navMenu.querySelectorAll('a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });
}

// ============================================
// PROJECT FILTERING
// ============================================

const filterButtons = document.querySelectorAll('.filter-btn');
const projectCards = document.querySelectorAll('.project-card');

if (filterButtons.length > 0) {
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // 모든 버튼에서 active 클래스 제거
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // 클릭된 버튼에 active 클래스 추가
            this.classList.add('active');

            const filterValue = this.getAttribute('data-filter');

            // 프로젝트 필터링
            projectCards.forEach(card => {
                if (filterValue === 'all') {
                    card.style.display = 'block';
                    setTimeout(() => {
                        card.style.opacity = '1';
                    }, 10);
                } else {
                    const category = card.getAttribute('data-category');
                    if (category === filterValue) {
                        card.style.display = 'block';
                        setTimeout(() => {
                            card.style.opacity = '1';
                        }, 10);
                    } else {
                        card.style.opacity = '0';
                        setTimeout(() => {
                            card.style.display = 'none';
                        }, 300);
                    }
                }
            });
        });
    });
}

// 프로젝트 카드에 트랜지션 추가
projectCards.forEach(card => {
    card.style.transition = 'opacity 0.3s ease';
    card.style.opacity = '1';
});

// ============================================
// CONTACT FORM SUBMISSION
// ============================================

const contactForm = document.getElementById('contactForm');

if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();

        // 폼 데이터 수집
        const formData = new FormData(this);
        const data = {
            name: formData.get('name'),
            email: formData.get('email'),
            subject: formData.get('subject'),
            message: formData.get('message')
        };

        // 폼 검증
        if (!data.name || !data.email || !data.subject || !data.message) {
            showFormMessage('모든 필드를 입력해주세요.', 'error');
            return;
        }

        // 이메일 검증
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(data.email)) {
            showFormMessage('유효한 이메일 주소를 입력해주세요.', 'error');
            return;
        }

        // 여기서는 실제로 서버로 전송하지 않고 로컬에서만 처리합니다
        // 실제 구현에서는 fetch를 사용하여 백엔드로 전송합니다
        
        // 콘솔에 메시지 출력 (데모 목적)
        console.log('Contact message:', data);

        // 성공 메시지 표시
        showFormMessage('메시지를 보내주셔서 감사합니다! 곧 연락드리겠습니다.', 'success');

        // 폼 리셋
        this.reset();

        // 3초 후 메시지 숨기기
        setTimeout(() => {
            const messageElement = document.getElementById('formMessage');
            if (messageElement) {
                messageElement.classList.remove('success', 'error');
                messageElement.textContent = '';
            }
        }, 3000);
    });
}

function showFormMessage(message, type) {
    const messageElement = document.getElementById('formMessage');
    if (messageElement) {
        messageElement.textContent = message;
        messageElement.classList.remove('success', 'error');
        messageElement.classList.add(type);
    }
}

// ============================================
// NAVIGATION ACTIVE STATE
// ============================================

function updateActiveNavigation() {
    const navLinks = document.querySelectorAll('.nav-menu a');
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
}

// 페이지 로드 시 활성 네비게이션 업데이트
document.addEventListener('DOMContentLoaded', updateActiveNavigation);

// ============================================
// SMOOTH SCROLL
// ============================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href !== '#' && document.querySelector(href)) {
            e.preventDefault();
            document.querySelector(href).scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// ============================================
// SCROLL ANIMATIONS
// ============================================

const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'slideInUp 0.6s ease forwards';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// 스크롤 애니메이션 적용
document.querySelectorAll('.skill-card, .project-item, .interest-card, .edu-card').forEach(element => {
    observer.observe(element);
});

// ============================================
// HEADER SCROLL EFFECT
// ============================================

const navbar = document.querySelector('.navbar');
let lastScroll = 0;

if (navbar) {
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 100) {
            navbar.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.15)';
        } else {
            navbar.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.08)';
        }

        lastScroll = currentScroll;
    });
}

// ============================================
// MOBILE NAVIGATION STYLES
// ============================================

const style = document.createElement('style');
style.textContent = `
    @media (max-width: 768px) {
        .nav-menu {
            position: fixed;
            left: -100%;
            top: 70px;
            flex-direction: column;
            background-color: white;
            width: 100%;
            text-align: center;
            transition: 0.3s;
            box-shadow: 0 10px 27px rgba(0, 0, 0, 0.05);
            gap: 0;
            padding: 2rem 0;
        }

        .nav-menu.active {
            left: 0;
        }

        .nav-menu a {
            display: block;
            padding: 1rem;
            border: none !important;
        }

        .nav-menu a:hover,
        .nav-menu a.active {
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            border-bottom: none !important;
        }
    }
`;
document.head.appendChild(style);

// ============================================
// PAGE LOAD ANIMATION
// ============================================

window.addEventListener('load', function() {
    document.body.style.opacity = '1';
});

// ============================================
// UTILITY FUNCTIONS
// ============================================

// 외부 링크 새 탭에서 열기
document.querySelectorAll('a[target="_blank"]').forEach(link => {
    if (!link.href.startsWith('#')) {
        link.addEventListener('click', function(e) {
            // 링크가 실제로 작동하도록 함
        });
    }
});

// ============================================
// SCROLL TO TOP BUTTON
// ============================================

// 스크롤 버튼 생성
const scrollTopButton = document.createElement('button');
scrollTopButton.innerHTML = '↑';
scrollTopButton.className = 'scroll-to-top';
scrollTopButton.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    font-size: 24px;
    display: none;
    z-index: 999;
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
`;

document.body.appendChild(scrollTopButton);

window.addEventListener('scroll', function() {
    if (window.pageYOffset > 300) {
        scrollTopButton.style.display = 'flex';
        scrollTopButton.style.alignItems = 'center';
        scrollTopButton.style.justifyContent = 'center';
    } else {
        scrollTopButton.style.display = 'none';
    }
});

scrollTopButton.addEventListener('click', function() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

scrollTopButton.addEventListener('mouseenter', function() {
    this.style.transform = 'scale(1.1)';
});

scrollTopButton.addEventListener('mouseleave', function() {
    this.style.transform = 'scale(1)';
});

// ============================================
// INITIALIZATION
// ============================================

console.log('Profile website loaded successfully!');
