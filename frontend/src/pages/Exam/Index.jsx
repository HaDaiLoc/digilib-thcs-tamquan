import React, { useState } from 'react';
import BookCard from '../../components/cards/BookCard'; // Tận dụng lại Card cũ hoặc tạo ExamCard mới

const ExamPage = () => {
  const exams = [
    { id: 1, title: "Đề cương ôn tập Toán 9 - Học kỳ 1", author: "Tổ Toán", category: "Toán", grade: "Khối 9", type: "Đề cương", image: "https://img.freepik.com/free-vector/math-concept-illustration_114360-3916.jpg" },
    { id: 2, title: "Đề thi thử Ngữ Văn vào 10 - Năm 2024", author: "Tổ Văn", category: "Văn", grade: "Khối 9", type: "Đề thi", image: "https://lh5.googleusercontent.com/proxy/f0vR2hyba-gjH4NdoLRWhMDYUDjf8_nd2fyjPUDDzwLpEG7Cbhzi8MCSr70k9vXJf4zYKJxPf9ZIpbQxpO5-CeNg3OGLuZLpg2WtPkjD00Wkj8wEkmCvnOMMIuooN1kzer_hXB7IOpzsdYr-W1nOx0XrThi4zaFnknE7QvjteA" },
    { id: 3, title: "Bộ câu hỏi trắc nghiệm Sử 8", author: "Thầy Bình", category: "Sử", grade: "Khối 8", type: "Trắc nghiệm", image: "https://img.freepik.com/free-vector/history-concept-illustration_114360-1123.jpg" },
    { id: 4, title: "Đề thi học kỳ 2 Tiếng Anh 7", author: "Cô Mai", category: "Anh", grade: "Khối 7", type: "Đề thi", image: "https://img.freepik.com/free-vector/english-teacher-concept-illustration_114360-7477.jpg" },
  ];

  const [filterType, setFilterType] = useState("Tất cả");

  const filteredExams = filterType === "Tất cả" 
    ? exams 
    : exams.filter(ex => ex.type === filterType);

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Banner nhỏ cho trang đề thi */}
      <div className="bg-gradient-to-r from-orange-400 to-red-500 rounded-2xl p-8 mb-10 text-white shadow-lg">
        <h1 className="text-3xl font-bold mb-2">Ngân Hàng Đề Thi & Đề Cương 📝</h1>
        <p className="opacity-90">Tổng hợp các bộ đề thi thử và tài liệu ôn tập sát với chương trình học.</p>
      </div>

      <div className="flex flex-col md:flex-row gap-8">
        {/* Bộ lọc nhanh bên trái */}
        <aside className="w-full md:w-64 space-y-6">
          <div className="bg-white p-5 rounded-xl shadow-sm border">
            <h3 className="font-bold mb-4 text-gray-800">Phân loại</h3>
            <div className="flex flex-col gap-3">
              {["Tất cả", "Đề cương", "Đề thi", "Trắc nghiệm"].map(type => (
                <button 
                  key={type}
                  onClick={() => setFilterType(type)}
                  className={`text-left px-4 py-2 rounded-lg text-sm transition ${filterType === type ? 'bg-orange-100 text-orange-600 font-bold' : 'text-gray-600 hover:bg-gray-50'}`}
                >
                  {type}
                </button>
              ))}
            </div>
          </div>
        </aside>

        {/* Danh sách đề thi */}
        <div className="flex-1">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredExams.map((exam) => (
              <BookCard 
                key={exam.id}
                title={exam.title}
                author={exam.author}
                category={exam.type} // Hiển thị loại đề ở phần nhãn
                image={exam.image}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExamPage;