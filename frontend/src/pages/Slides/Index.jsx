import React, { useEffect, useState } from 'react';
import BookCard from '../../components/cards/BookCard';
import { getDocumentsBySection, getUniqueSubjects } from '../../services/apiService';

const SlidePage = () => {
  const [slides, setSlides] = useState([]);
  const [subjects, setSubjects] = useState(['Tất cả']);
  const [filterType, setFilterType] = useState("Tất cả");
  const [selectedGrade, setSelectedGrade] = useState('Tất cả');

  useEffect(() => {
    let isMounted = true;

    const loadData = async () => {
      const [nextSlides, nextSubjects] = await Promise.all([
        getDocumentsBySection('slides'),
        getUniqueSubjects('slides'),
      ]);

      if (isMounted) {
        setSlides(nextSlides);
        setSubjects(['Tất cả', ...nextSubjects]);
      }
    };

    loadData();

    return () => {
      isMounted = false;
    };
  }, []);

  const filteredSlides = filterType === "Tất cả" 
    ? slides.filter((slide) => selectedGrade === 'Tất cả' || slide.grade === selectedGrade)
    : slides.filter(s => s.subject === filterType && (selectedGrade === 'Tất cả' || s.grade === selectedGrade));

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
              {subjects.map(type => (
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

          <div className="bg-white p-5 rounded-xl shadow-sm border">
            <h3 className="font-bold mb-4 text-gray-800">Khối lớp</h3>
            <div className="flex flex-col gap-3">
              {["Tất cả", "Khối 6", "Khối 7", "Khối 8", "Khối 9"].map(grade => (
                <button 
                  key={grade}
                  onClick={() => setSelectedGrade(grade)}
                  className={`text-left px-4 py-2 rounded-lg text-sm transition ${selectedGrade === grade ? 'bg-indigo-100 text-indigo-600 font-bold' : 'text-gray-600 hover:bg-gray-50'}`}
                >
                  {grade}
                </button>
              ))}
            </div>
          </div>
        </aside>

        <div className="flex-1">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredSlides.map((slide) => (
              <BookCard key={slide.id} document={slide} />
            ))}
          </div>

          {filteredSlides.length === 0 ? (
            <div className="text-center py-16 bg-white rounded-xl border border-dashed text-gray-400 mt-6">
              Chưa có slide phù hợp với bộ lọc hiện tại.
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default SlidePage;