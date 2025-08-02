// DOM 載入完成後執行
document.addEventListener('DOMContentLoaded', function() {
    // FAQ 互動功能
    initFAQ();
    
    // 滾動動畫
    initScrollAnimations();
    
    // 導航欄滾動效果
    initNavbarScroll();
    
    // 按鈕點擊效果
    initButtonEffects();
});

// FAQ 展開/收合功能 - 優化版本
function initFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer');
        
        // 預先計算內容高度
        const content = answer.querySelector('p');
        const contentHeight = content.scrollHeight;
        
        // 設置 CSS 自訂屬性，用於動畫
        answer.style.setProperty('--content-height', contentHeight + 'px');
        
        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            
            // 關閉所有其他 FAQ 項目（使用動畫）
            faqItems.forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains('active')) {
                    closeItem(otherItem);
                }
            });
            
            // 切換當前項目狀態
            if (isActive) {
                closeItem(item);
            } else {
                openItem(item);
            }
        });
    });
}

// 打開 FAQ 項目
function openItem(item) {
    const answer = item.querySelector('.faq-answer');
    const contentHeight = answer.style.getPropertyValue('--content-height');
    
    item.classList.add('active');
    answer.style.maxHeight = contentHeight;
    
    // 添加硬件加速
    answer.style.transform = 'translateZ(0)';
}

// 關閉 FAQ 項目
function closeItem(item) {
    const answer = item.querySelector('.faq-answer');
    
    // 直接設置為 0，讓 CSS transition 處理動畫
    answer.style.maxHeight = '0px';
    
    // 立即移除 active 類，讓 CSS 處理 padding 的動畫
    item.classList.remove('active');
}

// 滾動動畫效果
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // 觀察需要動畫的元素
    const animateElements = document.querySelectorAll(`
        .hero-title,
        .hero-description,
        .section-title,
        .section-description,
        .feature-card,
        .security-item,
        .faq-item
    `);
    
    animateElements.forEach(el => {
        observer.observe(el);
    });
}

// 導航欄滾動時的樣式變化
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    let lastScrollY = window.scrollY;
    
    window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY;
        
        if (currentScrollY > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        // 滾動方向檢測（可用於隱藏/顯示導航欄）
        if (currentScrollY > lastScrollY && currentScrollY > 300) {
            navbar.classList.add('nav-hidden');
        } else {
            navbar.classList.remove('nav-hidden');
        }
        
        lastScrollY = currentScrollY;
    });
}

// 按鈕點擊效果
function initButtonEffects() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // 創建漣漪效果
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            // 移除漣漪效果
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// 平滑滾動到指定區塊
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        const offsetTop = section.offsetTop - 80; // 導航欄高度補償
        window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
        });
    }
}

// 數字計數動畫效果
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    const timer = setInterval(() => {
        start += increment;
        element.textContent = Math.floor(start);
        
        if (start >= target) {
            element.textContent = target;
            clearInterval(timer);
        }
    }, 16);
}

// 添加加載動畫
function showLoadingSpinner(element) {
    element.innerHTML = '<div class="loading-spinner"></div>';
}

function hideLoadingSpinner(element, originalContent) {
    element.innerHTML = originalContent;
}

// 工具函數：防抖
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 工具函數：節流
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// 響應式處理
function handleResize() {
    const isMobile = window.innerWidth <= 768;
    
    // 根據螢幕大小調整某些行為
    if (isMobile) {
        document.body.classList.add('mobile');
    } else {
        document.body.classList.remove('mobile');
    }
}

// 監聽視窗大小變化
window.addEventListener('resize', debounce(handleResize, 250));

// 初始化響應式處理
handleResize();

// 表單驗證（如果有表單的話）
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('error');
            isValid = false;
        } else {
            input.classList.remove('error');
        }
    });
    
    return isValid;
}

// 錯誤處理
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// 成功提示
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = message;
    document.body.appendChild(successDiv);
    
    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}

// 模擬 API 調用
async function simulateAPICall(endpoint, data = null) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            // 模擬 90% 成功率
            if (Math.random() > 0.1) {
                resolve({
                    success: true,
                    data: { message: '操作成功' }
                });
            } else {
                reject(new Error('網路錯誤，請稍後再試'));
            }
        }, 1000 + Math.random() * 2000);
    });
}

// 懶加載圖片
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// 添加鍵盤導航支援
function initKeyboardNavigation() {
    document.addEventListener('keydown', (e) => {
        // ESC 鍵關閉 FAQ
        if (e.key === 'Escape') {
            const activeFAQ = document.querySelector('.faq-item.active');
            if (activeFAQ) {
                activeFAQ.classList.remove('active');
            }
        }
        
        // Enter 鍵觸發按鈕點擊
        if (e.key === 'Enter' && e.target.classList.contains('faq-question')) {
            e.target.click();
        }
    });
}

// 初始化鍵盤導航
initKeyboardNavigation();

// 性能監控
function initPerformanceMonitoring() {
    // 監控 LCP (Largest Contentful Paint)
    new PerformanceObserver((entryList) => {
        for (const entry of entryList.getEntries()) {
            console.log('LCP:', entry.startTime);
        }
    }).observe({ entryTypes: ['largest-contentful-paint'] });
    
    // 監控 FID (First Input Delay)
    new PerformanceObserver((entryList) => {
        for (const entry of entryList.getEntries()) {
            console.log('FID:', entry.processingStart - entry.startTime);
        }
    }).observe({ entryTypes: ['first-input'] });
}