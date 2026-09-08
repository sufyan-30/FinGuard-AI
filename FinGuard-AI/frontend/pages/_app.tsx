import '@/styles/globals.css';
import type { AppProps } from 'next/app';
import Link from 'next/link';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold text-blue-600">
            FinGuard AI
          </Link>
          <div className="flex gap-6">
            <Link href="/" className="text-gray-700 hover:text-blue-600 font-medium">
              Dashboard
            </Link>
            <Link href="/vendors" className="text-gray-700 hover:text-blue-600 font-medium">
              Vendors
            </Link>
            <Link href="/invoices" className="text-gray-700 hover:text-blue-600 font-medium">
              Invoices
            </Link>
            <Link href="/audit" className="text-gray-700 hover:text-blue-600 font-medium">
              Audit
            </Link>
          </div>
        </div>
      </nav>

      {/* Page Content */}
      <Component {...pageProps} />
    </div>
  );
}
