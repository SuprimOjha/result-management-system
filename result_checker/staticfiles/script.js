// Mobile Menu Toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const navLinks = document.querySelector('.nav-links');
const navButtons = document.querySelector('.nav-buttons');

if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
        mobileMenuBtn.classList.toggle('active');
        // You can add mobile menu functionality here
        console.log('Mobile menu clicked');
    });
}

// Result Form Submission
const resultForm = document.getElementById('resultForm');

if (resultForm) {
    resultForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const regNumber = document.getElementById('regNumber').value;
        const examType = document.getElementById('examType').value;
        
        if (!regNumber || !examType) {
            alert('Please fill in all fields');
            return;
        }
        
        // Show loading state
        const submitBtn = resultForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Loading...';
        submitBtn.disabled = true;
        
        // Simulate API call
        setTimeout(() => {
            // Mock result data
            displayResult({
                regNumber: regNumber,
                examType: examType,
                studentName: 'John Doe',
                subjects: [
                    { name: 'Mathematics', marks: 85, grade: 'A' },
                    { name: 'English', marks: 78, grade: 'B+' },
                    { name: 'Science', marks: 92, grade: 'A+' },
                    { name: 'History', marks: 80, grade: 'A-' },
                    { name: 'Computer Science', marks: 88, grade: 'A' }
                ],
                totalMarks: 423,
                percentage: 84.6,
                overallGrade: 'A',
                status: 'Pass'
            });
            
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }, 1500);
    });
}

// Display Result Function
function displayResult(data) {
    // Create modal for result display
    const modal = document.createElement('div');
    modal.className = 'result-modal';
    modal.innerHTML = `
        <div class="modal-overlay" onclick="closeResultModal()"></div>
        <div class="modal-content">
            <button class="modal-close" onclick="closeResultModal()">&times;</button>
            <div class="result-header">
                <h2>Examination Result</h2>
                <div class="result-info">
                    <p><strong>Registration Number:</strong> ${data.regNumber}</p>
                    <p><strong>Student Name:</strong> ${data.studentName}</p>
                    <p><strong>Examination:</strong> ${getExamTypeName(data.examType)}</p>
                </div>
            </div>
            <div class="result-body">
                <table class="result-table">
                    <thead>
                        <tr>
                            <th>Subject</th>
                            <th>Marks</th>
                            <th>Grade</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.subjects.map(subject => `
                            <tr>
                                <td>${subject.name}</td>
                                <td>${subject.marks}</td>
                                <td><span class="grade-badge grade-${subject.grade.replace('+', 'plus').replace('-', 'minus')}">${subject.grade}</span></td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
                <div class="result-summary">
                    <div class="summary-item">
                        <span class="summary-label">Total Marks:</span>
                        <span class="summary-value">${data.totalMarks}/500</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">Percentage:</span>
                        <span class="summary-value">${data.percentage}%</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">Overall Grade:</span>
                        <span class="summary-value grade-badge grade-${data.overallGrade}">${data.overallGrade}</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">Status:</span>
                        <span class="summary-value status-${data.status.toLowerCase()}">${data.status}</span>
                    </div>
                </div>
            </div>
            <div class="result-footer">
                <button class="btn-primary" onclick="downloadResult()">
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                        <path d="M10 2V14M10 14L6 10M10 14L14 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M2 14V16C2 17.1 2.9 18 4 18H16C17.1 18 18 17.1 18 16V14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                    Download PDF
                </button>
                <button class="btn-outline" onclick="printResult()">
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                        <path d="M5 6V2H15V6M5 14H3C2.4 14 2 13.6 2 13V9C2 8.4 2.4 8 3 8H17C17.6 8 18 8.4 18 9V13C18 13.6 17.6 14 17 14H15M5 11H15V18H5V11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    Print
                </button>
            </div>
        </div>
    `;
    
    // Add modal styles
    const style = document.createElement('style');
    style.textContent = `
        .result-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 9999;
            display: flex;
            justify-content: center;
            align-items: center;
            animation: fadeIn 0.3s ease;
        }
        
        .modal-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(5px);
        }
        
        .modal-content {
            position: relative;
            background: white;
            border-radius: 16px;
            max-width: 800px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            animation: slideUp 0.3s ease;
        }
        
        .modal-close {
            position: absolute;
            top: 20px;
            right: 20px;
            background: #F3F4F6;
            border: none;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            font-size: 24px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }
        
        .modal-close:hover {
            background: #E5E7EB;
            transform: rotate(90deg);
        }
        
        .result-header {
            padding: 40px 40px 24px;
            border-bottom: 2px solid #E5E7EB;
        }
        
        .result-header h2 {
            font-size: 28px;
            margin-bottom: 20px;
            color: #1F2937;
        }
        
        .result-info {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .result-info p {
            color: #6B7280;
            font-size: 14px;
        }
        
        .result-body {
            padding: 32px 40px;
        }
        
        .result-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 32px;
        }
        
        .result-table th {
            background: #F9FAFB;
            padding: 16px;
            text-align: left;
            font-weight: 600;
            color: #1F2937;
            border-bottom: 2px solid #E5E7EB;
        }
        
        .result-table td {
            padding: 16px;
            border-bottom: 1px solid #E5E7EB;
            color: #374151;
        }
        
        .result-table tr:last-child td {
            border-bottom: none;
        }
        
        .grade-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 12px;
        }
        
        .grade-Aplus, .grade-A {
            background: #D1FAE5;
            color: #065F46;
        }
        
        .grade-Aminus, .grade-Bplus {
            background: #DBEAFE;
            color: #1E40AF;
        }
        
        .grade-B, .grade-Bminus {
            background: #FEF3C7;
            color: #92400E;
        }
        
        .result-summary {
            background: #F9FAFB;
            border-radius: 12px;
            padding: 24px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        
        .summary-item {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .summary-label {
            color: #6B7280;
            font-size: 14px;
            font-weight: 500;
        }
        
        .summary-value {
            color: #1F2937;
            font-size: 20px;
            font-weight: 700;
        }
        
        .status-pass {
            color: #059669;
        }
        
        .status-fail {
            color: #DC2626;
        }
        
        .result-footer {
            padding: 24px 40px;
            border-top: 2px solid #E5E7EB;
            display: flex;
            gap: 16px;
            justify-content: center;
        }
        
        .result-footer button {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideUp {
            from {
                transform: translateY(50px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        @media (max-width: 768px) {
            .modal-content {
                width: 95%;
                max-height: 95vh;
            }
            
            .result-header,
            .result-body,
            .result-footer {
                padding-left: 20px;
                padding-right: 20px;
            }
            
            .result-summary {
                grid-template-columns: 1fr;
            }
            
            .result-footer {
                flex-direction: column;
            }
            
            .result-footer button {
                width: 100%;
                justify-content: center;
            }
        }
    `;
    
    document.head.appendChild(style);
    document.body.appendChild(modal);
    document.body.style.overflow = 'hidden';
}

function closeResultModal() {
    const modal = document.querySelector('.result-modal');
    if (modal) {
        modal.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => {
            modal.remove();
            document.body.style.overflow = 'auto';
        }, 300);
    }
}

function getExamTypeName(type) {
    const types = {
        'semester1': 'Semester 1 Examination',
        'semester2': 'Semester 2 Examination',
        'annual': 'Annual Examination',
        'midterm': 'Mid-term Examination'
    };
    return types[type] || type;
}

function downloadResult() {
    alert('Downloading result as PDF...\n\nNote: In a production environment, this would generate and download a PDF file.');
}

function printResult() {
    window.print();
}

// File Upload Handling
const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const uploadBtn = document.getElementById('uploadBtn');

if (fileInput && uploadArea) {
    // Drag and drop functionality
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#6366F1';
        uploadArea.style.background = '#F0F9FF';
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#E5E7EB';
        uploadArea.style.background = 'white';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#E5E7EB';
        uploadArea.style.background = 'white';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });
}

function handleFileSelect(file) {
    const validTypes = [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel',
        'text/csv'
    ];
    
    if (!validTypes.includes(file.type)) {
        alert('Please upload a valid Excel file (.xlsx, .xls, or .csv)');
        return;
    }
    
    // Show file info
    const uploadText = document.querySelector('.upload-text');
    uploadText.textContent = `Selected: ${file.name}`;
    uploadBtn.disabled = false;
    uploadBtn.style.opacity = '1';
    
    console.log('File selected:', file.name);
}

if (uploadBtn) {
    uploadBtn.addEventListener('click', () => {
        if (!fileInput.files || fileInput.files.length === 0) {
            alert('Please select a file first');
            return;
        }
        
        uploadBtn.textContent = 'Uploading...';
        uploadBtn.disabled = true;
        
        // Simulate upload
        setTimeout(() => {
            alert('File uploaded successfully! Results are now available for students to check.');
            uploadBtn.textContent = 'Upload Results';
            uploadBtn.disabled = true;
            fileInput.value = '';
            document.querySelector('.upload-text').textContent = 'Click to upload or drag and drop';
        }, 2000);
    });
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
        }
    });
}, observerOptions);

// Observe elements
document.querySelectorAll('.feature-card, .step-card').forEach(el => {
    el.style.opacity = '0';
    observer.observe(el);
});

// Add fadeInUp animation
const animationStyle = document.createElement('style');
animationStyle.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
`;
document.head.appendChild(animationStyle);

console.log('Student Results Portal initialized successfully!');