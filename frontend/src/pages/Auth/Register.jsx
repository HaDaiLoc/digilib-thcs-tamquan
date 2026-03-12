import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    fullName: '',
    studentId: '',
    grade: 'Khối 6',
    email: '',
    password: '',
    confirmPassword: ''
  });

  const handleRegister = (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      alert("Mật khẩu xác nhận không khớp!");
      return;
    }
    console.log("Dữ liệu đăng ký:", formData);
    alert("Đăng ký thành công! Chào mừng bạn đến với DigiLib.");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4">
      <div className="max-w-md w-full space-y-8 bg-white p-10 rounded-2xl shadow-lg border border-gray-100">
        <div className="text-center">
          <h2 className="text-3xl font-extrabold text-gray-900">Tạo tài khoản mới</h2>
          <p className="mt-2 text-sm text-gray-600">Gia nhập cộng đồng học tập Tam Quan</p>
        </div>

        <form className="mt-8 space-y-4" onSubmit={handleRegister}>
          <div className="space-y-3">
            <div>
              <label className="text-sm font-semibold text-gray-700">Họ và Tên</label>
              <input
                type="text"
                required
                className="appearance-none rounded-lg relative block w-full px-3 py-2 border border-gray-300 outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="Nguyễn Văn A"
                onChange={(e) => setFormData({...formData, fullName: e.target.value})}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-semibold text-gray-700">Mã số HS</label>
                <input
                  type="text"
                  required
                  className="appearance-none rounded-lg relative block w-full px-3 py-2 border border-gray-300 outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="2024HS001"
                  onChange={(e) => setFormData({...formData, studentId: e.target.value})}
                />
              </div>
              <div>
                <label className="text-sm font-semibold text-gray-700">Khối</label>
                <select 
                  className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 sm:text-sm"
                  onChange={(e) => setFormData({...formData, grade: e.target.value})}
                >
                  <option>Khối 6</option>
                  <option>Khối 7</option>
                  <option>Khối 8</option>
                  <option>Khối 9</option>
                </select>
              </div>
            </div>

            <div>
              <label className="text-sm font-semibold text-gray-700">Email</label>
              <input
                type="email"
                required
                className="appearance-none rounded-lg relative block w-full px-3 py-2 border border-gray-300 outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="hocsinh@thcstamquan.edu.vn"
                onChange={(e) => setFormData({...formData, email: e.target.value})}
              />
            </div>

            <div>
              <label className="text-sm font-semibold text-gray-700">Mật khẩu</label>
              <input
                type="password"
                required
                className="appearance-none rounded-lg relative block w-full px-3 py-2 border border-gray-300 outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="********"
                onChange={(e) => setFormData({...formData, password: e.target.value})}
              />
            </div>

            <div>
              <label className="text-sm font-semibold text-gray-700">Xác nhận mật khẩu</label>
              <input
                type="password"
                required
                className="appearance-none rounded-lg relative block w-full px-3 py-2 border border-gray-300 outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="********"
                onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full flex justify-center py-3 px-4 border border-transparent text-sm font-bold rounded-lg text-white bg-blue-600 hover:bg-blue-700 transition-all shadow-md hover:shadow-lg"
          >
            Đăng ký tài khoản
          </button>
        </form>

        <div className="text-center">
          <p className="text-sm text-gray-600">
            Đã có tài khoản?{' '}
            <Link to="/login" className="font-medium text-blue-600 hover:text-blue-500">
              Đăng nhập tại đây
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;