import React, { useState } from 'react';
import BookCard from '../../components/cards/BookCard';

const SlidePage = () => {
  const slides = [
    { id: 1, title: "Slide Bài giảng: Hệ thức lượng trong tam giác", author: "Thầy Tùng", category: "Toán", grade: "Khối 9", type: "Toán", image: "https://img.freepik.com/free-vector/presentation-concept-illustration_114360-155.jpg" },
    { id: 2, title: "Slide Ngữ Văn: Phân tích bài thơ Đồng Chí", author: "Cô Lan", category: "Văn", grade: "Khối 9", type: "Văn", image: "https://img.freepik.com/free-vector/blogging-concept-illustration_114360-788.jpg" },
    { id: 3, title: "Slide Vật Lý: Quang học và thấu kính", author: "Thầy Hùng", category: "Lý", grade: "Khối 9", type: "Lý", image: "https://img.freepik.com/free-vector/science-concept-illustration_114360-5381.jpg" },
  ];

  const [filterType, setFilterType] = useState("Tất cả");

  const filteredSlides = filterType === "Tất cả" 
    ? slides 
    : slides.filter(s => s.type === filterType);

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="bg-gradient-to-r from-blue-500 to-indigo-600 rounded-2xl p-8 mb-10 text-white shadow-lg">
        <h1 className="text-3xl font-bold mb-2">Slide Bài Giảng Điện Tử 💻</h1>
        <p className="opacity-90">Hỗ trợ học sinh ôn tập kiến thức qua các bài giảng trực quan.</p>
      </div>

      <div className="flex flex-col md:flex-row gap-8">
        <aside className="w-full md:w-64 space-y-6">
          <div className="bg-white p-5 rounded-xl shadow-sm border">
            <h3 className="font-bold mb-4 text-gray-800">Môn học</h3>
            <div className="flex flex-col gap-3">
              {["Tất cả", "Toán", "Văn", "Lý"].map(type => (
                <button 
                  key={type}
                  onClick={() => setFilterType(type)}
                  className={`text-left px-4 py-2 rounded-lg text-sm transition ${filterType === type ? 'bg-blue-100 text-blue-600 font-bold' : 'text-gray-600 hover:bg-gray-50'}`}
                >
                  {type}
                </button>
              ))}
            </div>
          </div>
        </aside>

        <div className="flex-1">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredSlides.map((slide) => (
              <BookCard 
                key={slide.id}
                title={slide.title}
                author={slide.author}
                category={slide.type}
                image={slide.image}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SlidePage;