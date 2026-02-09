"use client";

import { useEffect, useState } from "react";
import {
    CreditCard,
    ArrowUpRight,
    ArrowDownLeft,
    Search,
    Download,
    Filter,
    Loader2,
    DollarSign,
    TrendingUp
} from "lucide-react";
import { apiFetch } from "@/lib/api";

export default function FinancePage() {
    const [payments, setPayments] = useState<any[]>([]);
    const [stats, setStats] = useState<any>({ total_revenue: 0, monthly_revenue: 0 });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const [paymentsData, statsData] = await Promise.all([
                    apiFetch("/finance/payments/all"),
                    apiFetch("/finance/stats")
                ]);
                setPayments(paymentsData);
                setStats(statsData);
            } catch (err: any) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-2xl font-bold text-brand-navy">Finance & Fees</h2>
                    <p className="text-gray-500">Track revenue and student payment history</p>
                </div>
                <div className="flex gap-3">
                    <button className="bg-white border text-gray-600 px-4 py-2 rounded-lg font-semibold hover:bg-gray-50 transition-all flex items-center gap-2">
                        <Download className="w-4 h-4" />
                        Report
                    </button>
                    <button className="btn-primary flex items-center gap-2">
                        <CreditCard className="w-5 h-5" />
                        Record Payment
                    </button>
                </div>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div className="card flex items-center gap-4">
                    <div className="bg-brand-green-light p-3 rounded-xl text-brand-green">
                        <DollarSign className="w-6 h-6" />
                    </div>
                    <div>
                        <p className="text-xs text-gray-500 font-bold uppercase">Total Revenue</p>
                        <h4 className="text-2xl font-black text-brand-navy">
                            ${stats.total_revenue.toLocaleString()}
                        </h4>
                    </div>
                </div>
                <div className="card flex items-center gap-4">
                    <div className="bg-blue-50 p-3 rounded-xl text-blue-600">
                        <TrendingUp className="w-6 h-6" />
                    </div>
                    <div>
                        <p className="text-xs text-gray-500 font-bold uppercase">This Month</p>
                        <h4 className="text-2xl font-black text-brand-navy">
                            ${stats.monthly_revenue.toLocaleString()}
                        </h4>
                    </div>
                </div>
            </div>

            {/* Analytics & Reports Section */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 card">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="font-bold text-brand-navy">Revenue Analytics</h3>
                        <select className="bg-gray-50 border-none text-xs font-semibold px-2 py-1 rounded outline-none">
                            <option>Last 6 Months</option>
                            <option>Last Year</option>
                        </select>
                    </div>
                    {/* Simulated Chart */}
                    <div className="h-48 flex items-end gap-2 px-2">
                        {[40, 65, 45, 90, 85, 100].map((h, i) => (
                            <div key={i} className="flex-1 flex flex-col items-center gap-2 group">
                                <div
                                    className="w-full bg-brand-green-light rounded-t-lg group-hover:bg-brand-green transition-all"
                                    style={{ height: `${h}%` }}
                                ></div>
                                <span className="text-[10px] text-gray-400 font-bold">
                                    {['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'][i]}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="card">
                    <h3 className="font-bold text-brand-navy mb-4">Financial Documents</h3>
                    <div className="space-y-3">
                        {[
                            { name: "Term 1 Balance Sheet", size: "2.4MB" },
                            { name: "Annual Audit 2025", size: "5.1MB" },
                            { name: "Expense Summary Q4", size: "1.2MB" },
                        ].map((doc) => (
                            <div key={doc.name} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg group cursor-pointer hover:bg-brand-green-light transition-colors">
                                <div className="flex items-center gap-3">
                                    <div className="bg-white p-2 rounded border border-gray-100 group-hover:border-brand-green">
                                        <Download className="w-4 h-4 text-gray-400 group-hover:text-brand-green" />
                                    </div>
                                    <div>
                                        <p className="text-sm font-bold text-brand-navy transition-colors">{doc.name}</p>
                                        <p className="text-[10px] text-gray-400">{doc.size}</p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            <div className="space-y-4">
                <div className="flex items-center justify-between">
                    <h3 className="text-lg font-bold text-brand-navy">Recent Payments</h3>
                    <div className="flex items-center gap-2">
                        <div className="relative">
                            <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                            <input
                                type="text"
                                placeholder="Search payment..."
                                className="pl-9 pr-4 py-2 bg-white border border-gray-100 rounded-lg text-sm outline-none focus:ring-2 focus:ring-brand-green"
                            />
                        </div>
                        <button className="p-2 border border-gray-100 rounded-lg hover:bg-gray-50">
                            <Filter className="w-5 h-5 text-gray-400" />
                        </button>
                    </div>
                </div>

                <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden min-h-[200px] flex flex-col">
                    {loading ? (
                        <div className="flex-1 flex flex-col items-center justify-center gap-4">
                            <Loader2 className="w-8 h-8 text-brand-green animate-spin" />
                            <p className="text-gray-500 font-medium">Fetching transactions...</p>
                        </div>
                    ) : error ? (
                        <div className="flex-1 flex flex-col items-center justify-center gap-2 text-red-600">
                            <p className="font-bold">Failed to load payments</p>
                            <p className="text-sm">{error}</p>
                        </div>
                    ) : (
                        <table className="w-full text-left">
                            <thead className="bg-gray-50 border-b">
                                <tr>
                                    <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Amount</th>
                                    <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Date</th>
                                    <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Method</th>
                                    <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Reference</th>
                                    <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Action</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y text-sm">
                                {payments.length === 0 ? (
                                    <tr>
                                        <td colSpan={5} className="px-6 py-12 text-center text-gray-500">
                                            No recent transactions found.
                                        </td>
                                    </tr>
                                ) : (
                                    payments.map((p) => (
                                        <tr key={p.id} className="hover:bg-gray-50 transition-colors">
                                            <td className="px-6 py-4 font-mono font-bold text-brand-green">
                                                ${p.amount_paid.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                                            </td>
                                            <td className="px-6 py-4 text-gray-500">
                                                {new Date(p.payment_date).toLocaleDateString()}
                                            </td>
                                            <td className="px-6 py-4">
                                                <span className="bg-blue-50 text-blue-700 px-2 py-1 rounded text-[10px] uppercase font-bold">
                                                    {p.payment_method}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 text-gray-400 font-mono text-xs">
                                                {p.reference_number || "N/A"}
                                            </td>
                                            <td className="px-6 py-4">
                                                <button className="text-brand-navy hover:text-brand-green underline transition-colors">
                                                    Receipt
                                                </button>
                                            </td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </table>
                    )}
                </div>
            </div>
        </div>
    );
}
