import React from 'react';

const BookCard = ({ title, author, category, image }) => {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow group cursor-pointer">
      {/* Hình ảnh sách */}
      <div className="h-48 bg-gray-200 relative overflow-hidden">
        <img 
          src={image || "https://via.placeholder.com/150x200?text=No+Cover"} 
          alt={title}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
        />
        <span className="absolute top-2 right-2 bg-blue-600 text-white text-[10px] font-bold px-2 py-1 rounded">
          {category}
        </span>
      </div>

      {/* Thông tin sách */}
      <div className="p-4">
        <h3 className="font-bold text-gray-800 line-clamp-1 mb-1 group-hover:text-blue-600">
          {title}
        </h3>
        <p className="text-sm text-gray-500 mb-4 italic">GV: {author}</p>
        
        <button className="w-full py-2 bg-blue-50 text-blue-600 rounded-lg text-sm font-semibold hover:bg-blue-600 hover:text-white transition-colors">
          Xem tài liệu
        </button>
      </div>
    </div>
  );
};

export default BookCard;