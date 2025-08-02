# Whoscall 數位名片官網

基於 Figma 設計稿開發的 Whoscall 數位名片官方網站，採用原生 HTML、CSS、JavaScript 實現，具備完整的響應式設計和互動效果。

## 🚀 功能特色

- **響應式設計**：完美適配桌面端、平板和手機
- **現代化 UI**：基於 Figma 設計稿的像素級還原
- **流暢動畫**：豐富的滾動動畫和互動效果
- **優秀性能**：原生代碼實現，加載速度快
- **無障礙支援**：支援鍵盤導航和螢幕閱讀器
- **SEO 友好**：語義化 HTML 結構

## 📁 項目結構

```
cursor_Whoscall_Pass/
├── index.html          # 主頁面
├── styles.css          # 樣式文件
├── script.js           # JavaScript 功能
└── README.md           # 項目說明
```

## 🎨 設計實現

### 頁面區塊
1. **導航欄** - 品牌 Logo + 下載按鈕
2. **英雄區** - 主標題、描述文字與手機展示
3. **統計數據** - 用戶信任度統計
4. **數位名片功能** - 核心功能介紹
5. **綠勾勾認證** - 信任標記說明
6. **來電目的詢問** - 溝通優化功能
7. **安全性介紹** - 三大安全保障
8. **四大特色功能** - 核心賣點展示
9. **安全性重點** - 詳細安全說明
10. **FAQ 區塊** - 常見問題解答
11. **頁腳** - 版權與連結

### 技術特點
- **CSS Grid & Flexbox** - 現代化佈局
- **CSS Variables** - 統一的設計系統
- **Intersection Observer** - 高效滾動動畫
- **防抖節流** - 優化性能體驗
- **語義化標籤** - 提升 SEO 與無障礙

## 🛠️ 開發說明

### 樣式架構
- 採用 BEM 命名規範
- 使用 CSS 自定義屬性管理主題
- 移動端優先的響應式設計
- 系統化的間距和尺寸規範

### JavaScript 功能
- FAQ 展開收合
- 滾動動畫觸發
- 導航欄滾動效果
- 按鈕漣漪效果
- 鍵盤導航支援
- 性能監控

### 響應式斷點
- Desktop: > 768px
- Tablet: 768px
- Mobile: < 480px

## 🚀 使用方法

1. 直接在瀏覽器中打開 `index.html`
2. 或使用本地服務器運行：

```bash
# 使用 Python
python -m http.server 8000

# 使用 Node.js
npx serve .

# 使用 PHP
php -S localhost:8000
```

## 🎯 瀏覽器支援

- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

## 📱 移動端優化

- Touch 友好的交互設計
- 優化的字體大小和行高
- 合適的點擊區域大小
- 流暢的滾動體驗

## ⚡ 性能優化

- 原生代碼實現，無框架依賴
- 圖片使用 SVG 和 Base64 減少請求
- CSS 和 JS 文件合併壓縮
- 懶加載和預載入策略

## 🔧 自定義配置

### 主題顏色
在 `styles.css` 中修改 CSS 變量：

```css
:root {
    --primary-color: #00CC66;
    --primary-dark: #00B359;
    /* ... 其他顏色變量 */
}
```

### 動畫效果
在 `script.js` 中調整動畫參數：

```javascript
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};
```

## 📄 授權

本項目基於 Whoscall 官方設計稿開發，僅供學習和展示使用。

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request 來改進這個項目。

---

*開發時間：2024年*  
*技術架構：原生 HTML + CSS + JavaScript*