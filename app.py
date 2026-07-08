import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import io
import zipfile
import base64
import time

# Page configuration
st.set_page_config(
    page_title="Lower Third Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #020617 50%, #111827 100%);
        background-attachment: fixed;
    }
    
    /* Animated background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(ellipse at 20% 20%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 80%, rgba(6, 182, 212, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 50%, rgba(59, 130, 246, 0.05) 0%, transparent 70%);
        pointer-events: none;
        z-index: -1;
        animation: pulse 8s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {
        visibility: visible;
        background: transparent !important;
    }

    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"] {
        visibility: hidden !important;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6, p, span, div {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Glassmorphism Card */
    .glass-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(139, 92, 246, 0.4);
        box-shadow: 
            0 12px 40px rgba(139, 92, 246, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.08);
        transform: translateY(-2px);
    }
    
    /* Hero Title */
    .hero-title {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 50%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: glow 3s ease-in-out infinite;
    }
    
    @keyframes glow {
        0%, 100% { filter: drop-shadow(0 0 20px rgba(139, 92, 246, 0.3)); }
        50% { filter: drop-shadow(0 0 40px rgba(6, 182, 212, 0.5)); }
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.2rem;
        color: #cbd5e1;
        text-align: center;
        font-weight: 300;
        letter-spacing: 0.05em;
    }
    
    /* Section Title */
    .section-title {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.5rem;
        font-weight: 600;
        color: #f8fafc;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .section-title::before {
        content: '';
        width: 4px;
        height: 24px;
        background: linear-gradient(180deg, #8b5cf6, #06b6d4);
        border-radius: 2px;
    }
    
    /* Upload Area */
    .upload-zone {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
        border: 2px dashed rgba(139, 92, 246, 0.4);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .upload-zone:hover {
        border-color: #8b5cf6;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(6, 182, 212, 0.15) 100%);
        box-shadow: 0 0 30px rgba(139, 92, 246, 0.2);
    }
    
    .upload-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .upload-text {
        color: #f8fafc;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .upload-hint {
        color: #64748b;
        font-size: 0.9rem;
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .status-badge.success {
        background: rgba(34, 197, 94, 0.15);
        color: #22c55e;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    
    .status-badge.processing {
        background: rgba(139, 92, 246, 0.15);
        color: #8b5cf6;
        border: 1px solid rgba(139, 92, 246, 0.3);
    }
    
    .status-badge.info {
        background: rgba(6, 182, 212, 0.15);
        color: #06b6d4;
        border: 1px solid rgba(6, 182, 212, 0.3);
    }

    .status-badge.warning {
        background: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    .status-badge.error {
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    /* Stats Card */
    .stats-card {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 1.25rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stats-card:hover {
        border-color: rgba(6, 182, 212, 0.4);
        transform: scale(1.02);
    }
    
    .stats-number {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #8b5cf6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stats-label {
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 0.25rem;
    }
    
    /* Preview Card */
    .preview-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(139, 92, 246, 0.15);
        border-radius: 16px;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .preview-card:hover {
        border-color: rgba(6, 182, 212, 0.5);
        transform: scale(1.02);
        box-shadow: 0 20px 40px rgba(139, 92, 246, 0.2);
    }
    
    .preview-card img {
        transition: transform 0.4s ease;
    }
    
    .preview-card:hover img {
        transform: scale(1.05);
    }
    
    .preview-caption {
        padding: 1rem;
        color: #cbd5e1;
        font-size: 0.9rem;
        font-weight: 500;
        background: rgba(0, 0, 0, 0.3);
        text-align: center;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    /* Progress Bar */
    .progress-container {
        background: rgba(15, 23, 42, 0.8);
        border-radius: 10px;
        padding: 0.25rem;
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 8px;
        border-radius: 8px;
        background: linear-gradient(90deg, #8b5cf6, #06b6d4, #3b82f6);
        background-size: 200% 100%;
        animation: shimmer 2s linear infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    /* Download Button */
    .download-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%);
        color: white !important;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        text-decoration: none;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
    }
    
    .download-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5);
    }
    
    /* Streamlit overrides */
    .stFileUploader {
        background: transparent !important;
    }
    
    .stFileUploader > div > div {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%) !important;
        border: 2px dashed rgba(139, 92, 246, 0.4) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #8b5cf6 !important;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(6, 182, 212, 0.15) 100%) !important;
    }

    .stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] {
        display: none !important;
    }

    .stFileUploader [data-testid="stFileUploaderDropzone"] {
        justify-content: center !important;
        gap: 0 !important;
    }

    .stFileUploader [data-testid="stFileUploaderDropzone"] button {
        position: relative !important;
        color: transparent !important;
        font-size: 0 !important;
        width: 168px !important;
        min-width: 168px !important;
        height: 44px !important;
        min-height: 44px !important;
        margin: 0 !important;
        padding: 0 !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%) !important;
        box-shadow: 0 10px 24px rgba(6, 182, 212, 0.18), 0 4px 14px rgba(139, 92, 246, 0.22) !important;
        text-align: center !important;
        overflow: hidden !important;
        transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease !important;
    }

    .stFileUploader [data-testid="stFileUploaderDropzone"] button:hover {
        transform: translateY(-1px) !important;
        filter: brightness(1.06) !important;
        box-shadow: 0 14px 28px rgba(6, 182, 212, 0.22), 0 7px 18px rgba(139, 92, 246, 0.28) !important;
    }

    .stFileUploader [data-testid="stFileUploaderDropzone"] button:active {
        transform: translateY(0) !important;
    }

    .stFileUploader [data-testid="stFileUploaderDropzone"] button::after {
        content: "Choose Images";
        color: white !important;
        position: absolute !important;
        inset: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        line-height: 44px !important;
        text-align: center !important;
        width: 100% !important;
        letter-spacing: 0 !important;
        pointer-events: none !important;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4) !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5) !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(2, 6, 23, 0.98) 100%) !important;
        border-right: 1px solid rgba(139, 92, 246, 0.2) !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding: 1.25rem 1rem 2rem 1rem;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #cbd5e1 !important;
    }

    .sidebar-brand {
        padding: 1.25rem 0 1rem 0;
        text-align: center;
    }

    .sidebar-logo {
        width: 52px;
        height: 52px;
        border-radius: 16px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 0.75rem;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.25), rgba(6, 182, 212, 0.18));
        border: 1px solid rgba(139, 92, 246, 0.35);
        box-shadow: 0 12px 28px rgba(6, 182, 212, 0.12);
        font-size: 1.7rem;
    }

    .sidebar-title {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.25rem;
        font-weight: 700;
        background: linear-gradient(135deg, #f8fafc, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .sidebar-subtitle {
        color: #94a3b8;
        font-size: 0.78rem;
        margin-top: 0.2rem;
    }

    .sidebar-panel {
        padding: 1rem;
        margin: 0.9rem 0;
        background: rgba(15, 23, 42, 0.58);
        border: 1px solid rgba(148, 163, 184, 0.14);
        border-radius: 14px;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
    }

    .sidebar-section-title {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        color: #f8fafc;
        font-weight: 700;
        font-size: 0.88rem;
        letter-spacing: 0.01em;
        margin-bottom: 0.85rem;
    }

    .sidebar-section-title span {
        width: 28px;
        height: 28px;
        border-radius: 10px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: rgba(6, 182, 212, 0.12);
        border: 1px solid rgba(6, 182, 212, 0.2);
    }

    .sidebar-helper {
        color: #94a3b8;
        font-size: 0.8rem;
        line-height: 1.45;
        margin: -0.25rem 0 0.8rem 0;
    }

    .sidebar-status {
        color: #22c55e;
        background: rgba(34, 197, 94, 0.12);
        border: 1px solid rgba(34, 197, 94, 0.24);
        border-radius: 10px;
        padding: 0.65rem 0.75rem;
        font-size: 0.78rem;
        line-height: 1.35;
        word-break: break-word;
        margin-top: 0.75rem;
    }

    [data-testid="stSidebar"] .stFileUploader > div > div {
        border-radius: 12px !important;
        padding: 0.85rem !important;
        min-height: 92px !important;
    }

    [data-testid="stSidebar"] .stFileUploader [data-testid="stFileUploaderDropzone"] button {
        width: 126px !important;
        min-width: 126px !important;
        height: 38px !important;
        min-height: 38px !important;
        border-radius: 10px !important;
        box-shadow: 0 8px 18px rgba(6, 182, 212, 0.15), 0 3px 10px rgba(139, 92, 246, 0.2) !important;
    }

    [data-testid="stSidebar"] .stFileUploader [data-testid="stFileUploaderDropzone"] button::after {
        content: "Choose PNG";
        font-size: 0.84rem !important;
        line-height: 38px !important;
    }

    [data-testid="stSidebar"] .stFileUploader small {
        color: #94a3b8 !important;
    }

    [data-testid="stSidebar"] .stSlider,
    [data-testid="stSidebar"] .stCheckbox,
    [data-testid="stSidebar"] .stFileUploader {
        margin-bottom: 0.35rem;
    }
    
    /* Divider */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.3), rgba(6, 182, 212, 0.3), transparent);
        margin: 2rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #64748b;
        font-size: 0.85rem;
    }
    
    .footer a {
        color: #8b5cf6;
        text-decoration: none;
    }
    
    /* Alert/Error/Success boxes */
    .stSuccess {
        background: rgba(34, 197, 94, 0.15) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        border-radius: 12px !important;
        color: #22c55e !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.15) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 12px !important;
        color: #ef4444 !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.15) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 12px !important;
        color: #f59e0b !important;
    }
    
    .stInfo {
        background: rgba(6, 182, 212, 0.15) !important;
        border: 1px solid rgba(6, 182, 212, 0.3) !important;
        border-radius: 12px !important;
        color: #06b6d4 !important;
    }
    
    /* Image styling */
    [data-testid="stImage"] {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(139, 92, 246, 0.2);
        transition: all 0.3s ease;
    }
    
    [data-testid="stImage"]:hover {
        border-color: rgba(6, 182, 212, 0.4);
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.2);
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #8b5cf6, #06b6d4) !important;
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        color: #cbd5e1 !important;
    }
</style>
""", unsafe_allow_html=True)

components.html(
    """
    <script>
    (() => {
        const doc = window.parent.document;
        const buttonId = "lower-third-sidebar-toggle";
        const hiddenClass = "lower-third-sidebar-hidden";

        let style = doc.getElementById("lower-third-sidebar-toggle-style");
        if (!style) {
            style = doc.createElement("style");
            style.id = "lower-third-sidebar-toggle-style";
            doc.head.appendChild(style);
        }

        style.textContent = `
                #${buttonId} {
                    position: fixed;
                    top: 16px;
                    left: 16px;
                    z-index: 2147483647;
                    width: 42px;
                    height: 42px;
                    border: 1px solid rgba(148, 163, 184, 0.22);
                    border-radius: 12px;
                    background: linear-gradient(135deg, rgba(139, 92, 246, 0.98), rgba(6, 182, 212, 0.98));
                    color: #fff;
                    box-shadow: 0 14px 32px rgba(6, 182, 212, 0.22), 0 6px 18px rgba(0, 0, 0, 0.28);
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                    transition: left 0.22s ease, transform 0.18s ease, filter 0.18s ease;
                }

                #${buttonId}:hover {
                    transform: translateY(-1px);
                    filter: brightness(1.08);
                }

                #${buttonId} svg {
                    width: 20px;
                    height: 20px;
                    stroke-width: 2.4;
                }

                body.${hiddenClass} [data-testid="stSidebar"] {
                    min-width: 0 !important;
                    width: 0 !important;
                    transform: translateX(-100%) !important;
                    opacity: 0 !important;
                    overflow: hidden !important;
                    pointer-events: none !important;
                }

                body:not(.${hiddenClass}) [data-testid="stSidebar"] {
                    display: block !important;
                    visibility: visible !important;
                    min-width: 21rem !important;
                    width: 21rem !important;
                    opacity: 1 !important;
                    transform: translateX(0) !important;
                    pointer-events: auto !important;
                    overflow: visible !important;
                }

                body:not(.${hiddenClass}) [data-testid="stSidebar"] * {
                    visibility: visible !important;
                }
            `;

        let button = doc.getElementById(buttonId);
        if (!button) {
            button = doc.createElement("button");
            button.id = buttonId;
            button.type = "button";
            doc.body.appendChild(button);
        }

        const icons = {
            open: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"></rect><path d="M7 20h10M3 12h18"></path></svg>`,
            closed: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"></rect><path d="M7 20h10M3 12h18"></path></svg>`
        };

        const positionButton = () => {
            const sidebar = doc.querySelector('[data-testid="stSidebar"]');
            const hidden = doc.body.classList.contains(hiddenClass);
            if (sidebar && !hidden) {
                button.style.left = `${Math.max(sidebar.getBoundingClientRect().width + 16, 58)}px`;
            } else {
                button.style.left = "16px";
            }
        };

        const render = () => {
            const hidden = doc.body.classList.contains(hiddenClass);
            button.innerHTML = hidden ? icons.closed : icons.open;
            button.setAttribute("aria-label", hidden ? "Show sidebar" : "Hide sidebar");
            button.title = hidden ? "Show sidebar" : "Hide sidebar";
            positionButton();
        };

        const hideLeakedMaterialIconText = () => {
            const leakedIconNames = new Set([
                "keyboard_double_arrow_left",
                "keyboard_double_arrow_right"
            ]);

            doc.querySelectorAll('button, [role="button"], span, div').forEach((element) => {
                const text = (element.textContent || "").trim();
                if (!leakedIconNames.has(text)) {
                    return;
                }

                const nativeButton = element.closest('button, [role="button"]') || element;
                if (nativeButton.id !== buttonId) {
                    nativeButton.style.display = "none";
                    nativeButton.setAttribute("aria-hidden", "true");
                }
            });
        };

        const openNativeSidebar = () => {
            const controls = Array.from(doc.querySelectorAll('button, [role="button"]'));
            const openControl = controls.find((control) => {
                const label = `${control.getAttribute("aria-label") || ""} ${control.title || ""}`.toLowerCase();
                return label.includes("open sidebar") || label.includes("show sidebar") || label.includes("expand sidebar");
            });
            if (openControl) {
                openControl.click();
            }
        };

        window.localStorage.removeItem("lowerThirdSidebarHidden");
        doc.body.classList.remove(hiddenClass);
        openNativeSidebar();
        hideLeakedMaterialIconText();
        render();

        button.onclick = () => {
            const willShow = doc.body.classList.contains(hiddenClass);
            doc.body.classList.toggle(hiddenClass);
            if (willShow) {
                openNativeSidebar();
            }
            render();
        };

        window.parent.addEventListener("resize", positionButton);
        const observer = new MutationObserver(hideLeakedMaterialIconText);
        observer.observe(doc.body, { childList: true, subtree: true });
        setTimeout(hideLeakedMaterialIconText, 100);
        setTimeout(hideLeakedMaterialIconText, 500);
        setTimeout(hideLeakedMaterialIconText, 1000);
        setTimeout(openNativeSidebar, 100);
        setTimeout(openNativeSidebar, 500);
        setTimeout(positionButton, 300);
        setTimeout(positionButton, 1000);
    })();
    </script>
    """,
    height=0,
)

# Error handling helper functions
def show_error(title: str, message: str, suggestion: str = None):
    """Display a styled error message with optional suggestion"""
    st.markdown(f"""
    <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 12px; padding: 1rem; margin: 1rem 0;">
        <div style="color: #ef4444; font-weight: 600; margin-bottom: 0.5rem;">❌ {title}</div>
        <div style="color: #fca5a5; font-size: 0.95rem; margin-bottom: 0.5rem;">{message}</div>
        {f'<div style="color: #94a3b8; font-size: 0.85rem; margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid rgba(239, 68, 68, 0.2;">💡 <strong>Suggestion:</strong> {suggestion}</div>' if suggestion else ''}
    </div>
    """, unsafe_allow_html=True)

def show_warning(title: str, message: str):
    """Display a styled warning message"""
    st.markdown(f"""
    <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 12px; padding: 1rem; margin: 1rem 0;">
        <div style="color: #f59e0b; font-weight: 600; margin-bottom: 0.5rem;">⚠️ {title}</div>
        <div style="color: #fcd34d; font-size: 0.95rem;">{message}</div>
    </div>
    """, unsafe_allow_html=True)

def show_success(message: str):
    """Display a styled success message"""
    st.markdown(f"""
    <div style="background: rgba(34, 197, 94, 0.15); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 12px; padding: 1rem; margin: 1rem 0;">
        <div style="color: #22c55e; font-weight: 600;">✅ {message}</div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">🎬</div>
        <div class="sidebar-title">Thirds From The Grey</div>
        <div class="sidebar-subtitle">6ix Level</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-panel">
        <div class="sidebar-section-title"><span>⚙️</span>Settings</div>
    """, unsafe_allow_html=True)
    
    output_quality = st.slider("Output Quality", 70, 100, 95, help="JPEG quality for exported images")
    
    show_preview = st.checkbox("Show Preview Gallery", value=True, help="Display processed images")

    st.markdown("""
        <div class="sidebar-section-title" style="margin-top: 1.1rem;"><span>🖼️</span>Lower Third PNG</div>
        <div class="sidebar-helper">Use a transparent PNG overlay, or leave this empty to use the default file.</div>
    """, unsafe_allow_html=True)

    custom_overlay_file = st.file_uploader(
        "Custom lower third PNG",
        type=["png"],
        accept_multiple_files=False,
        help="Upload a transparent PNG lower third to use instead of the default overlay.",
        label_visibility="collapsed"
    )

    if custom_overlay_file:
        st.markdown(f"""
        <div class="sidebar-status">
            Custom overlay loaded: {custom_overlay_file.name}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-panel">
        <div class="sidebar-section-title"><span>📊</span>Session Stats</div>
    """, unsafe_allow_html=True)
    
    if 'processed_count' not in st.session_state:
        st.session_state.processed_count = 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{st.session_state.processed_count}</div>
            <div class="stats-label">Processed</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{st.session_state.processed_count}</div>
            <div class="stats-label">Exported</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-panel">
        <div class="sidebar-section-title"><span>💡</span>Pro Tip</div>
        <div class="sidebar-helper" style="margin-bottom: 0;">
            Upload a transparent PNG lower third to brand every exported image.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main content
st.markdown("""
<div style="text-align: center; padding: 2rem 0 3rem 0;">
    <div class="hero-title">Thirds From The Grey</div>
    <div class="hero-subtitle">Grey World Overlays</div>
</div>
""", unsafe_allow_html=True)

# Feature badges
st.markdown("""
<div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-bottom: 2rem;">
    <span class="status-badge info">⚡ Batch Processing</span>
    <span class="status-badge processing">🎨 Auto-Scaling</span>
    <span class="status-badge info">🖼️ Custom PNG Overlay</span>
    <span class="status-badge success">📦 ZIP Export</span>
</div>
""", unsafe_allow_html=True)

# Main glass card
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown("""
<div class="section-title">Source Collection</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="color: #94a3b8; margin-bottom: 1.5rem; font-size: 0.95rem;">
    Slide your pics in, overlay gon' stick right away, no setup needed.
</div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Source image files",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

st.markdown('</div>', unsafe_allow_html=True)

# Processing section
if uploaded_files:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Stats row
    num_files = len(uploaded_files)
    st.markdown(f"""
    <div style="display: flex; justify-content: center; gap: 2rem; margin: 1.5rem 0; flex-wrap: wrap;">
        <div class="stats-card" style="min-width: 120px;">
            <div class="stats-number">{num_files}</div>
            <div class="stats-label">Images Queued</div>
        </div>
        <div class="stats-card" style="min-width: 120px;">
            <div class="stats-number">{'Custom' if custom_overlay_file else 'Default'}</div>
            <div class="stats-label">Overlay</div>
        </div>
        <div class="stats-card" style="min-width: 120px;">
            <div class="stats-number">{output_quality}%</div>
            <div class="stats-label">Quality</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Processing
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-title">⚡ Processing</div>
    """, unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    error_container = st.container()
    
    # Load overlay with improved error handling
    overlay = None
    overlay_error = False
    
    try:
        if custom_overlay_file:
            try:
                overlay = Image.open(io.BytesIO(custom_overlay_file.getvalue())).convert("RGBA")
            except Exception as e:
                overlay_error = True
                with error_container:
                    show_error(
                        "Invalid Custom Overlay",
                        f"Failed to load the uploaded PNG: {str(e)}",
                        "Ensure the file is a valid PNG image. Try re-uploading it."
                    )
        else:
            try:
                overlay = Image.open("lower_third.png").convert("RGBA")
            except FileNotFoundError:
                overlay_error = True
                with error_container:
                    show_error(
                        "Default Overlay Not Found",
                        "The default 'lower_third.png' file is missing from the server.",
                        "Upload a custom PNG overlay in Settings to proceed, or contact support."
                    )
            except Exception as e:
                overlay_error = True
                with error_container:
                    show_error(
                        "Cannot Read Default Overlay",
                        f"Error reading overlay file: {str(e)}",
                        "Try uploading a custom PNG overlay in Settings."
                    )
    except Exception as e:
        overlay_error = True
        with error_container:
            show_error(
                "Unexpected Error",
                f"An unexpected error occurred: {str(e)}",
                "Please try refreshing the page and try again."
            )
    
    if overlay_error or overlay is None:
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()
    
    zip_buffer = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED)
    
    processed_images = []
    successful_count = 0
    failed_count = 0
    failed_files = []
    
    for idx, file in enumerate(uploaded_files):
        progress = (idx + 1) / num_files
        progress_bar.progress(progress)
        status_text.markdown(f"""
        <div style="color: #8b5cf6; font-weight: 500;">
            Processing: {file.name} ({idx + 1}/{num_files})
        </div>
        """, unsafe_allow_html=True)
        
        try:
            # Try to open and validate the image
            base = Image.open(io.BytesIO(file.read())).convert("RGBA")
            
            # Validate image dimensions
            if base.width == 0 or base.height == 0:
                raise ValueError("Image has invalid dimensions (0x0)")
            
            if base.width > 8000 or base.height > 8000:
                show_warning(
                    f"Large Image: {file.name}",
                    "This image is very large and might take longer to process."
                )
        except Image.UnidentifiedImageError:
            failed_count += 1
            failed_files.append(file.name)
            with error_container:
                show_error(
                    f"Cannot Open: {file.name}",
                    "This file is not a valid image format or is corrupted.",
                    "Try re-exporting the image from your editor."
                )
            continue
        except ValueError as e:
            failed_count += 1
            failed_files.append(file.name)
            with error_container:
                show_error(
                    f"Invalid Image: {file.name}",
                    str(e),
                    "The image file appears to be corrupted. Try using a different file."
                )
            continue
        except Exception as e:
            failed_count += 1
            failed_files.append(file.name)
            with error_container:
                show_error(
                    f"Error Processing: {file.name}",
                    f"Unexpected error: {str(e)}",
                    "Try processing this file separately."
                )
            continue
        
        try:
            # Process the image
            scale = base.width / overlay.width
            overlay_resized = overlay.resize(
                (base.width, int(overlay.height * scale))
            )
            
            position = (0, base.height - overlay_resized.height)
            
            result = base.copy()
            result.paste(overlay_resized, position, overlay_resized)
            
            # Save to buffer with error handling
            img_buffer = io.BytesIO()
            result.convert("RGB").save(img_buffer, format="JPEG", quality=output_quality)
            
            # Add to ZIP
            zip_file.writestr(
                f"lowerthird_{file.name}.jpg",
                img_buffer.getvalue()
            )
            
            processed_images.append((result, file.name))
            successful_count += 1
            
        except Exception as e:
            failed_count += 1
            failed_files.append(file.name)
            with error_container:
                show_error(
                    f"Export Error: {file.name}",
                    f"Failed to save processed image: {str(e)}",
                    "This might be a memory issue. Try processing fewer files at once."
                )
            continue
        
        time.sleep(0.1)  # Smooth animation
    
    zip_file.close()
    
    st.session_state.processed_count = successful_count
    
    # Summary status
    if successful_count > 0:
        status_text.markdown(f"""
        <div class="status-badge success" style="display: inline-flex;">
            ✅ Successfully processed {successful_count}/{num_files} images
        </div>
        """, unsafe_allow_html=True)
    
    if failed_count > 0:
        with error_container:
            show_warning(
                f"⚠️ {failed_count} File(s) Failed",
                f"Failed files: {', '.join(failed_files[:3])}{'...' if len(failed_files) > 3 else ''}"
            )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Preview Gallery
    if show_preview and processed_images:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("""
        <div class="section-title">🖼️ Preview Gallery</div>
        """, unsafe_allow_html=True)
        
        # Responsive grid
        cols_per_row = 3 if num_files > 2 else num_files
        rows = [processed_images[i:i + cols_per_row] for i in range(0, len(processed_images), cols_per_row)]
        
        for row in rows:
            cols = st.columns(len(row))
            for col, (img, name) in zip(cols, row):
                with col:
                    st.image(img, caption=name, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Download section
    if successful_count > 0:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("""
        <div class="section-title">📥 Export</div>
        <div style="color: #94a3b8; margin-bottom: 1.5rem;">
            Your images are ready! Download the complete package below.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="⬇️  Download ZIP Package",
                data=zip_buffer.getvalue(),
                file_name="lowerthird_outputs.zip",
                mime="application/zip",
                use_container_width=True
            )
        
        st.markdown(f"""
        <div style="text-align: center; margin-top: 1rem; color: #64748b; font-size: 0.85rem;">
            📦 Package contains {successful_count} processed images at {output_quality}% quality
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Empty state
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0; color: #64748b;">
        <div style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.5;">📷</div>
        <div style="font-size: 1.1rem; margin-bottom: 0.5rem;">Nothing Here Yet</div>
        <div style="font-size: 0.9rem;">Add your images above to get started</div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    <div style="margin-bottom: 0.5rem;">
        <span style="background: linear-gradient(135deg, #8b5cf6, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 600;">
            Third From The Gray
        </span>
        <span style="color: #475569;"> • </span>
        <span>Raw Broadcast Visuals</span>
    </div>
    <div style="color: #475569; font-size: 0.8rem;">
        For the ones making content. Keep it moving.
    </div>
</div>
""", unsafe_allow_html=True)
