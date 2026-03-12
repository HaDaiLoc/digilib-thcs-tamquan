import React, { useState } from 'react';

const DonationPage = () => {
  const [formData, setFormData] = useState({
    fullName: '',
    bookName: '',
    grade: 'Khối 6',
    condition: 'Còn mới',
    message: ''
  });

  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Dữ liệu quyên góp:", formData);
    // Sau này sẽ gọi API gửi về Backend ở đây
    setSubmitted(true);
    
    // Reset form sau 3 giây
    setTimeout(() => setSubmitted(false), 3000);
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-12">
      <div className="grid md:grid-cols-2 gap-12 items-center">
        
        {/* Phần 1: Nội dung giới thiệu */}
        <div>
          <h1 className="text-4xl font-bold text-blue-600 mb-6">Góc Quyên Góp</h1>
          <p className="text-gray-600 text-lg mb-6 leading-relaxed">
            "Sách cũ của bạn là kho tàng tri thức của người khác." <br />
            Hãy cùng nhau xây dựng thư viện trường THCS Tam Quan ngày càng phong phú bằng cách chia sẻ những cuốn sách bạn đã đọc xong nhé!
          </p>
          <div className="space-y-4">
            <div className="flex items-start gap-4">
              <span className="bg-green-100 p-2 rounded-full">✅</span>
              <p className="text-gray-700">Tặng sách giáo khoa, sách tham khảo.</p>
            </div>
            <div className="flex items-start gap-4">
              <span className="bg-green-100 p-2 rounded-full">✅</span>
              <p className="text-gray-700">Chia sẻ đề cương, vở ghi chép đẹp.</p>
            </div>
          </div>
        </div>

        {/* Phần 2: Form quyên góp */}
        <div className="bg-white p-8 rounded-2xl shadow-xl border border-blue-50">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Thông tin quyên góp</h2>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Họ và tên của bạn</label>
              <input 
                required
                type="text" 
                className="w-full px-4 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Nguyễn Văn A"
                onChange={(e) => setFormData({...formData, fullName: e.target.value})}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Tên tài liệu/sách quyên góp</label>
              <input 
                required
                type="text" 
                className="w-full px-4 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Ví dụ: Sách Toán 9 nâng cao"
                onChange={(e) => setFormData({...formData, bookName: e.target.value})}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Dành cho khối</label>
                <select 
                  className="w-full px-4 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-blue-500"
                  onChange={(e) => setFormData({...formData, grade: e.target.value})}
                >
                  <option>Khối 6</option>
                  <option>Khối 7</option>
                  <option>Khối 8</option>
                  <option>Khối 9</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Tình trạng</label>
                <select 
                  className="w-full px-4 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-blue-500"
                  onChange={(e) => setFormData({...formData, condition: e.target.value})}
                >
                  <option>Còn mới</option>
                  <option>Đã sử dụng</option>
                  <option>Hơi cũ</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Lời nhắn (nếu có)</label>
              <textarea 
                rows="3"
                className="w-full px-4 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Chúc các em học tốt nhé."
                onChange={(e) => setFormData({...formData, message: e.target.value})}
              ></textarea>
            </div>

            <button 
              type="submit"
              className={`w-full py-3 rounded-lg font-bold text-white transition-all ${submitted ? 'bg-green-500' : 'bg-blue-600 hover:bg-blue-700'}`}
            >
              {submitted ? 'Đã gửi thành công! ✨' : 'Gửi thông tin quyên góp'}
            </button>
          </form>
        </div>

      </div>
    </div>
  );
};

export default DonationPage;