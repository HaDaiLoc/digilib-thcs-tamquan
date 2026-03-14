import React, { useEffect, useState } from 'react';
import BookCard from '../../components/cards/BookCard';
import { getDocumentsBySection, getUniqueSubjects } from '../../services/apiService';

const ExamPage = () => {
  const [exams, setExams] = useState([]);
  const [subjects, setSubjects] = useState(['Tất cả']);
  const [filterType, setFilterType] = useState('Tất cả');
  const [selectedGrade, setSelectedGrade] = useState('Tất cả');
  const [selectedSubject, setSelectedSubject] = useState('Tất cả');

  useEffect(() => {
    let isMounted = true;

    const loadData = async () => {
      const [nextExams, nextSubjects] = await Promise.all([
        getDocumentsBySection('exams'),
        getUniqueSubjects('exams'),
      ]);

      if (isMounted) {
        setExams(nextExams);
        setSubjects(['Tất cả', ...nextSubjects]);
      }
    };

    loadData();

    return () => {
      isMounted = false;
    };
  }, []);

  const filteredExams = exams.filter((exam) => {
    const matchType = filterType === 'Tất cả' || exam.resourceType === filterType;
    const matchGrade = selectedGrade === 'Tất cả' || exam.grade === selectedGrade;
    const matchSubject = selectedSubject === 'Tất cả' || exam.subject === selectedSubject;
    return matchType && matchGrade && matchSubject;
  });

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
              {["Tất cả", "Đề cương", "Đề thi"].map(type => (
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

          <div className="bg-white p-5 rounded-xl shadow-sm border">
            <h3 className="font-bold mb-4 text-gray-800">Khối lớp</h3>
            <div className="flex flex-col gap-3">
              {["Tất cả", "Khối 6", "Khối 7", "Khối 8", "Khối 9"].map(grade => (
                <button 
                  key={grade}
                  onClick={() => setSelectedGrade(grade)}
                  className={`text-left px-4 py-2 rounded-lg text-sm transition ${selectedGrade === grade ? 'bg-blue-100 text-blue-600 font-bold' : 'text-gray-600 hover:bg-gray-50'}`}
                >
                  {grade}
                </button>
              ))}
            </div>
          </div>

          <div className="bg-white p-5 rounded-xl shadow-sm border">
            <h3 className="font-bold mb-4 text-gray-800">Môn học</h3>
            <div className="flex flex-col gap-3">
              {subjects.map(subject => (
                <button 
                  key={subject}
                  onClick={() => setSelectedSubject(subject)}
                  className={`text-left px-4 py-2 rounded-lg text-sm transition ${selectedSubject === subject ? 'bg-emerald-100 text-emerald-600 font-bold' : 'text-gray-600 hover:bg-gray-50'}`}
                >
                  {subject}
                </button>
              ))}
            </div>
          </div>
        </aside>

        {/* Danh sách đề thi */}
        <div className="flex-1">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredExams.map((exam) => (
              <BookCard key={exam.id} document={exam} />
            ))}
          </div>

          {filteredExams.length === 0 ? (
            <div className="text-center py-16 bg-white rounded-xl border border-dashed text-gray-400 mt-6">
              Chưa có đề thi phù hợp với bộ lọc hiện tại.
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default ExamPage;