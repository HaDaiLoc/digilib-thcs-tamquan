import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import {
  getDocumentById,
  getSectionLabel,
  ROLE_LABELS,
  getApiErrorMessage,
} from '../../services/apiService';

const DocumentDetailPage = () => {
  const { documentId } = useParams();
  const [document, setDocument] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let isMounted = true;

    const loadDocument = async () => {
      try {
        const nextDocument = await getDocumentById(documentId);
        if (isMounted) {
          setDocument(nextDocument);
        }
      } catch (requestError) {
        if (isMounted) {
          setError(getApiErrorMessage(requestError, 'Không tải được tài liệu.'));
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    loadDocument();

    return () => {
      isMounted = false;
    };
  }, [documentId]);

  if (loading) {
    return <div className="max-w-4xl mx-auto px-4 py-16 text-center text-gray-500">Đang tải tài liệu...</div>;
  }

  if (!document) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center">
        <h1 className="text-3xl font-bold text-gray-800 mb-4">Không tìm thấy tài liệu</h1>
        <p className="text-gray-500 mb-6">{error || 'Tài liệu này có thể đã bị xóa hoặc đường dẫn không còn hợp lệ.'}</p>
        <Link
          to="/library"
          className="inline-flex items-center px-5 py-3 rounded-xl bg-blue-600 text-white font-semibold hover:bg-blue-700 transition"
        >
          Quay lại thư viện
        </Link>
      </div>
    );
  }

  const createdDate = new Date(document.createdAt).toLocaleDateString('vi-VN');

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <div className="grid lg:grid-cols-[360px,1fr] gap-10 items-start">
        <div className="bg-white border border-gray-100 rounded-3xl overflow-hidden shadow-sm">
          <div className="h-[420px] bg-gray-100">
            <img src={document.image} alt={document.title} className="w-full h-full object-cover" />
          </div>
        </div>

        <div>
          <div className="flex flex-wrap gap-3 mb-5">
            <span className="px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-sm font-semibold">
              {getSectionLabel(document.section)}
            </span>
            <span className="px-3 py-1 rounded-full bg-amber-50 text-amber-700 text-sm font-semibold">
              {document.resourceType}
            </span>
            <span className="px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 text-sm font-semibold">
              {document.subject}
            </span>
            <span className="px-3 py-1 rounded-full bg-slate-100 text-slate-700 text-sm font-semibold">
              {document.grade}
            </span>
          </div>

          <h1 className="text-4xl font-black text-gray-900 mb-4">{document.title}</h1>
          <p className="text-lg text-gray-600 leading-8 mb-8">{document.description}</p>

          <div className="grid sm:grid-cols-2 gap-4 mb-8">
            <div className="bg-white border border-gray-100 rounded-2xl p-5">
              <p className="text-xs uppercase tracking-[0.2em] text-gray-400 mb-2">Tác giả</p>
              <p className="text-gray-800 font-semibold">{document.author}</p>
            </div>
            <div className="bg-white border border-gray-100 rounded-2xl p-5">
              <p className="text-xs uppercase tracking-[0.2em] text-gray-400 mb-2">Đăng tải bởi</p>
              <p className="text-gray-800 font-semibold">
                {ROLE_LABELS[document.ownerRole]} - {document.createdByName}
              </p>
            </div>
            <div className="bg-white border border-gray-100 rounded-2xl p-5">
              <p className="text-xs uppercase tracking-[0.2em] text-gray-400 mb-2">Ngày đăng</p>
              <p className="text-gray-800 font-semibold">{createdDate}</p>
            </div>
            <div className="bg-white border border-gray-100 rounded-2xl p-5">
              <p className="text-xs uppercase tracking-[0.2em] text-gray-400 mb-2">Tệp tài liệu</p>
              <p className="text-gray-800 font-semibold">PDF trực tuyến</p>
            </div>
          </div>

          <div className="flex flex-wrap gap-4">
            <a
              href={document.pdfUrl}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center px-6 py-3 rounded-xl bg-blue-600 text-white font-semibold hover:bg-blue-700 transition"
            >
              Mở PDF
            </a>
            <a
              href={document.pdfUrl}
              download
              className="inline-flex items-center px-6 py-3 rounded-xl bg-white border border-gray-200 text-gray-800 font-semibold hover:bg-gray-50 transition"
            >
              Tải xuống
            </a>
            <Link
              to={`/${document.section === 'library' ? 'library' : document.section}`}
              className="inline-flex items-center px-6 py-3 rounded-xl bg-slate-100 text-slate-700 font-semibold hover:bg-slate-200 transition"
            >
              Quay lại danh mục
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentDetailPage;