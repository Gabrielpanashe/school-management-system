"use client";

import Link from "next/link";
import {
  ArrowRight,
  ShieldCheck,
  Zap,
  BarChart3,
  GraduationCap
} from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navbar */}
      <nav className="flex items-center justify-between px-8 py-6 max-w-7xl mx-auto">
        <div className="flex items-center gap-2">
          <div className="bg-brand-navy p-1.5 rounded-lg text-white">
            <GraduationCap className="w-6 h-6" />
          </div>
          <span className="text-xl font-bold text-brand-navy tracking-tight">SmartSchool</span>
        </div>

        <div className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-600">
          <a href="#" className="hover:text-brand-green transition-colors">Features</a>
          <a href="#" className="hover:text-brand-green transition-colors">Solutions</a>
          <a href="#" className="hover:text-brand-green transition-colors">Pricing</a>
        </div>

        <div className="flex items-center gap-4">
          <Link href="/login" className="text-sm font-semibold text-brand-navy hover:text-brand-green transition-colors px-4 py-2">
            Sign In
          </Link>
          <Link href="/register" className="btn-primary">
            Get Started
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="px-8 pt-20 pb-32 max-w-7xl mx-auto">
        <div className="text-center max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-green-light text-brand-green text-xs font-bold uppercase tracking-wider mb-6">
            <span className="flex h-2 w-2 rounded-full bg-brand-green"></span>
            Cloud-Based School ERP
          </div>
          <h1 className="text-5xl md:text-7xl font-extrabold text-brand-navy leading-tight mb-8">
            Manage your school <span className="text-brand-green italic">smarter</span>, not harder.
          </h1>
          <p className="text-lg text-gray-500 mb-10 leading-relaxed">
            The all-in-one platform for modern education. Handle admissions, attendance,
            grades, and fees with a beautiful, intuitive interface.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/register" className="btn-primary px-8 py-4 text-lg flex items-center gap-2 group">
              Register Your School
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link href="/login" className="px-8 py-4 text-lg font-semibold text-brand-navy hover:bg-gray-50 rounded-xl transition-all border border-gray-200">
              Admin Login
            </Link>
          </div>
        </div>
      </section>

      {/* Feature Section */}
      <section className="bg-brand-green-light py-24">
        <div className="max-w-7xl mx-auto px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="card border-none hover:translate-y-[-4px] transition-transform">
              <div className="bg-blue-100 text-blue-600 w-12 h-12 rounded-xl flex items-center justify-center mb-6">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold mb-3 text-brand-navy">Secure Records</h3>
              <p className="text-gray-500 text-sm">
                Multi-tenant architecture ensures student data is encrypted and isolated per institution.
              </p>
            </div>
            <div className="card border-none hover:translate-y-[-4px] transition-transform">
              <div className="bg-green-100 text-green-600 w-12 h-12 rounded-xl flex items-center justify-center mb-6">
                <Zap className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold mb-3 text-brand-navy">Real-time Stats</h3>
              <p className="text-gray-500 text-sm">
                Get instant insights into student performance and fee collection dashboard.
              </p>
            </div>
            <div className="card border-none hover:translate-y-[-4px] transition-transform">
              <div className="bg-purple-100 text-purple-600 w-12 h-12 rounded-xl flex items-center justify-center mb-6">
                <BarChart3 className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold mb-3 text-brand-navy">PDF Reports</h3>
              <p className="text-gray-500 text-sm">
                Generate professional report cards and fee receipts in one click with built-in PDF engine.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
