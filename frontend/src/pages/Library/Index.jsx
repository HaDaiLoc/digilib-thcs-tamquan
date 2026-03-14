import React, { useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import BookCard from '../../components/cards/BookCard';
import { getDocumentsBySection, getUniqueSubjects } from '../../services/apiService';

const LibraryPage = () => {
  const [searchParams] = useSearchParams();
  const [books, setBooks] = useState([]);
  const [subjects, setSubjects] = useState(['Tất cả']);
  const [selectedGrade, setSelectedGrade] = useState("Tất cả");
  const [selectedCategory, setSelectedCategory] = useState("Tất cả");
  const [keyword, setKeyword] = useState(searchParams.get('q') || '');

  useEffect(() => {
    let isMounted = true;

    const loadData = async () => {
      const [nextBooks, nextSubjects] = await Promise.all([
        getDocumentsBySection('library'),
        getUniqueSubjects('library'),
      ]);

      if (isMounted) {
        setBooks(nextBooks);
        setSubjects(['Tất cả', ...nextSubjects]);
      }
    };

    loadData();

    return () => {
      isMounted = false;
    };
  }, []);

  const filteredBooks = books.filter(book => {
    const matchGrade = selectedGrade === "Tất cả" || book.grade === selectedGrade;
    const matchCategory = selectedCategory === "Tất cả" || book.subject === selectedCategory;
    const normalizedKeyword = keyword.trim().toLowerCase();
    const matchKeyword =
      normalizedKeyword.length === 0 ||
      `${book.title} ${book.description} ${book.author} ${book.subject}`.toLowerCase().includes(normalizedKeyword);
    return matchGrade && matchCategory && matchKeyword;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Kho Tài Nguyên Số</h1>

      <div className="flex flex-col md:flex-row gap-8">
        <aside className="w-full md:w-64 flex-shrink-0">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 sticky top-24">
            <h2 className="font-bold text-lg mb-4 flex items-center gap-2">
              <span>🔍</span> Bộ lọc
            </h2>

            <div className="mb-6">
              <h3 className="font-semibold text-gray-700 mb-3 text-sm uppercase tracking-wider">Khối lớp</h3>
              <div className="space-y-2">
                {['Tất cả', 'Khối 6', 'Khối 7', 'Khối 8', 'Khối 9'].map((grade) => (
                  <label key={grade} className="flex items-center gap-2 cursor-pointer group">
                    <input 
                      type="radio" 
                      name="grade"
                      checked={selectedGrade === grade}
                      onChange={() => setSelectedGrade(grade)}
                      className="w-4 h-4 text-blue-600 focus:ring-blue-500" 
                    />
                    <span className={`text-sm ${selectedGrade === grade ? "text-blue-600 font-bold" : "text-gray-600"}`}>
                      {grade}
                    </span>
                  </label>
                ))}
              </div>
            </div>

            <div className="mb-6">
              <h3 className="font-semibold text-gray-700 mb-3 text-sm uppercase tracking-wider">Môn học</h3>
              <div className="space-y-2">
                {subjects.map((subject) => (
                  <label key={subject} className="flex items-center gap-2 cursor-pointer group">
                    <input
                      type="radio"
                      name="subject"
                      checked={selectedCategory === subject}
                      onChange={() => setSelectedCategory(subject)}
                      className="w-4 h-4 text-blue-600 focus:ring-blue-500"
                    />
                    <span className={`text-sm ${selectedCategory === subject ? "text-blue-600 font-bold" : "text-gray-600"}`}>
                      {subject}
                    </span>
                  </label>
                ))}
              </div>
            </div>

            <div className="mb-6">
              <h3 className="font-semibold text-gray-700 mb-3 text-sm uppercase tracking-wider">Từ khóa</h3>
              <input
                value={keyword}
                onChange={(event) => setKeyword(event.target.value)}
                className="w-full px-4 py-2 border border-gray-200 rounded-lg outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Tìm theo tiêu đề, môn, tác giả..."
              />
            </div>

            <button 
              onClick={() => { setSelectedGrade("Tất cả"); setSelectedCategory("Tất cả"); setKeyword(''); }}
              className="w-full py-2 bg-gray-100 text-gray-600 rounded-lg text-sm font-semibold hover:bg-gray-200 transition"
            >
              Xóa bộ lọc
            </button>
          </div>
        </aside>

        <div className="flex-1">
          <div className="flex justify-between items-center mb-6 bg-white p-4 rounded-lg shadow-sm border border-gray-50">
            <p className="text-sm text-gray-500 italic">Hiển thị {filteredBooks.length} kết quả</p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredBooks.map((book) => (
              <BookCard key={book.id} document={book} />
            ))}
          </div>
          
          {filteredBooks.length === 0 && (
            <div className="text-center py-20 bg-white rounded-xl border border-dashed">
              <p className="text-gray-400">Không tìm thấy tài liệu nào. Thử chọn khối khác bạn nhé! 📚</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LibraryPage;