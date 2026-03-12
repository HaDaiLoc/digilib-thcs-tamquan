import React, { useState } from 'react';
import BookCard from '../../components/cards/BookCard';

const LibraryPage = () => {
  const books = [
    { id: 1, title: "Toán học lớp 9 - Ôn thi vào 10", author: "Nguyễn Văn A", category: "Toán", grade: "Khối 9", image: "https://www.superprof.co.in/blog/wp-content/uploads/2021/09/image3-2.png" },
    { id: 2, title: "Ngữ văn: Tuyển tập các bài văn mẫu", author: "Trần Thị B", category: "Văn", grade: "Khối 9", image: "https://cbqqo.edu.vn/storage/app/public/photos/7/8xprovn_hieunh_170304100311images.jpg" },
    { id: 3, title: "Vật lý lớp 8: Cơ học nâng cao", author: "Lê Văn C", category: "Lý", grade: "Khối 8", image: "https://i.ytimg.com/vi/ZAqIoDhornk/maxresdefault.jpg" },
    { id: 4, title: "Tiếng Anh: Ngữ pháp cơ bản", author: "Phạm Anh D", category: "Anh", grade: "Khối 8", image: "https://img.freepik.com/free-vector/hand-drawn-english-book-background_23-2149483336.jpg?semt=ais_rp_progressive&w=740&q=80" },
    { id: 5, title: "Lịch sử Việt Nam thế kỷ XX", author: "Hoàng Văn E", category: "Sử", grade: "Khối 9", image: "https://cdn-media.sforum.vn/storage/app/media/wp-content/uploads/2024/02/nhung-cuon-sach-ve-lich-su-viet-nam-anh-dai-dien.jpg" },
  ];

  // Sửa lỗi chính tả "Tất cả" để khớp với logic bên dưới
  const [selectedGrade, setSelectedGrade] = useState("Tất cả");
  const [selectedCategory, setSelectedCategory] = useState("Tất cả");

  // Đổi allBooks thành books để khớp với biến đã khai báo bên trên
  const filteredBooks = books.filter(book => {
    const matchGrade = selectedGrade === "Tất cả" || book.grade === selectedGrade;
    const matchCategory = selectedCategory === "Tất cả" || book.category === selectedCategory;
    return matchGrade && matchCategory;
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
                {/* Thêm nút "Tất cả" vào để người dùng quay lại từ đầu */}
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

            <button 
              onClick={() => { setSelectedGrade("Tất cả"); setSelectedCategory("Tất cả"); }}
              className="w-full py-2 bg-gray-100 text-gray-600 rounded-lg text-sm font-semibold hover:bg-gray-200 transition"
            >
              Xóa bộ lọc
            </button>
          </div>
        </aside>

        <div className="flex-1">
          <div className="flex justify-between items-center mb-6 bg-white p-4 rounded-lg shadow-sm border border-gray-50">
            {/* Dùng filteredBooks.length để hiện số lượng sau khi lọc */}
            <p className="text-sm text-gray-500 italic">Hiển thị {filteredBooks.length} kết quả</p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {/* PHẢI DÙNG filteredBooks.map Ở ĐÂY */}
            {filteredBooks.map((book) => (
              <BookCard 
                key={book.id}
                title={book.title}
                author={book.author}
                category={book.category}
                image={book.image}
              />
            ))}
          </div>
          
          {/* Hiện thông báo nếu không có sách nào khớp bộ lọc */}
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