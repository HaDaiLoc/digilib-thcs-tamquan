import React from 'react';

const HomePage = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-700 to-blue-500 py-20 text-white text-center">
        <h1 className="text-5xl font-extrabold mb-4">Thư Viện Số Trường THCS Tam Quan</h1>
        <p className="text-xl mb-10 text-blue-100 italic">"Học, Học Nữa, Học Mãi"</p>
        
        <div className="max-w-2xl mx-auto px-4">
          <input 
            type="text" 
            placeholder="Tìm đề thi, giáo án, sách bài tập, ..." 
            className="w-full py-4 px-8 rounded-full text-gray-800 shadow-2xl focus:ring-4 focus:ring-blue-300 outline-none"
          />
        </div>
      </section>

      {/* Categories */}
      <section className="max-w-7xl mx-auto py-16 px-4">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {[
            { n: 'Ebooks', i: '📖', c: 'bg-blue-50' },
            { n: 'Đề thi & Đề cương', i: '📝', c: 'bg-green-50' },
            { n: 'Slide Bài giảng', i: '💻', c: 'bg-yellow-50' },
            { n: 'Góc Tặng sách', i: '🎁', c: 'bg-pink-50' },
          ].map((item, idx) => (
            <div key={idx} className={`${item.c} p-10 rounded-3xl text-center hover:scale-105 transition transform cursor-pointer border border-transparent hover:border-blue-200`}>
              <div className="text-5xl mb-4">{item.i}</div>
              <h3 className="font-bold text-gray-800 text-lg">{item.n}</h3>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default HomePage;