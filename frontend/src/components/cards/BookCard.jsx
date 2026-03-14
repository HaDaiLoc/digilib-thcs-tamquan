import React from 'react';
import { Link } from 'react-router-dom';
import { getSectionLabel } from '../../services/apiService';

const BookCard = ({ document }) => {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow group cursor-pointer">
      {/* Hình ảnh sách */}
      <div className="h-48 bg-gray-200 relative overflow-hidden">
        <img 
          src={document.image || "https://via.placeholder.com/150x200?text=No+Cover"} 
          alt={document.title}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
        />
        <span className="absolute top-2 right-2 bg-blue-600 text-white text-[10px] font-bold px-2 py-1 rounded">
          {document.resourceType}
        </span>
      </div>

      {/* Thông tin sách */}
      <div className="p-4">
        <p className="text-xs uppercase tracking-[0.2em] text-gray-400 mb-2">{getSectionLabel(document.section)}</p>
        <h3 className="font-bold text-gray-800 line-clamp-2 mb-1 min-h-[3.5rem] group-hover:text-blue-600">
          {document.title}
        </h3>
        <p className="text-sm text-gray-500 mb-1 italic">{document.author}</p>
        <p className="text-sm text-gray-500 mb-4">{document.subject} - {document.grade}</p>

        <Link
          to={`/documents/${document.id}`}
          className="block w-full py-2 bg-blue-50 text-blue-600 rounded-lg text-sm font-semibold hover:bg-blue-600 hover:text-white transition-colors text-center"
        >
          Xem tài liệu
        </Link>
      </div>
    </div>
  );
};

export default BookCard;