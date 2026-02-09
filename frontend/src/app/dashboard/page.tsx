"use client";

import { useEffect, useState } from "react";
import { Users, UserSquare2, CreditCard, BookOpen, Loader2 } from "lucide-react";
import { apiFetch } from "@/lib/api";

export default function DashboardPage() {
    const [stats, setStats] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // In a real scenario, we'd have a dashboard/stats endpoint
        // For now, let's simulate fetching students/teachers counts
        const fetchStats = async () => {
            try {
                // Mocking parallel fetch or a single stats endpoint
                // const [students, teachers] = await Promise.all([
                //   apiFetch("/students/"),
                //   apiFetch("/teachers/")
                // ]);
                setStats({
                    students: "1,240",
                    teachers: "48",
                    classes: "32",
                    fees: "85%"
                });
            } catch (err) {
                console.error("Failed to fetch dashboard stats", err);
            } finally {
                setLoading(false);
            }
        };

        fetchStats();
    }, []);

    if (loading) {
        return (
            <div className="flex h-[60vh] items-center justify-center">
                <Loader2 className="w-8 h-8 text-brand-green animate-spin" />
            </div>
        );
    }

    const statCards = [
        { name: "Total Students", value: stats?.students, icon: Users, color: "text-blue-600", bg: "bg-blue-50" },
        { name: "Total Teachers", value: stats?.teachers, icon: UserSquare2, color: "text-green-600", bg: "bg-green-50" },
        { name: "Classes", value: stats?.classes, icon: BookOpen, color: "text-purple-600", bg: "bg-purple-50" },
        { name: "Fees Paid", value: stats?.fees, icon: CreditCard, color: "text-amber-600", bg: "bg-amber-50" },
    ];

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {statCards.map((stat) => (
                    <div key={stat.name} className="card flex items-center gap-4 hover:border-brand-green transition-all cursor-pointer">
                        <div className={`${stat.bg} ${stat.color} p-4 rounded-xl`}>
                            <stat.icon className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-sm text-gray-500 font-medium">{stat.name}</p>
                            <p className="text-2xl font-bold text-brand-navy">{stat.value}</p>
                        </div>
                    </div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Performance Analytics */}
                <div className="card">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="text-lg font-bold text-brand-navy">Academic Performance</h3>
                        <span className="text-[10px] font-bold text-brand-green bg-brand-green-light px-2 py-1 rounded">Overall: +5.2%</span>
                    </div>
                    <div className="h-64 flex items-end justify-between gap-4 px-4 pb-2 border-b border-gray-100">
                        {[65, 82, 75, 88, 92].map((h, i) => (
                            <div key={i} className="flex-1 flex flex-col items-center gap-3 group">
                                <div
                                    className="w-full bg-brand-navy rounded-t-lg group-hover:bg-brand-green transition-all relative overflow-hidden"
                                    style={{ height: `${h}%` }}
                                >
                                    <div className="absolute inset-0 bg-white/10 group-hover:bg-transparent"></div>
                                </div>
                                <span className="text-[10px] text-gray-400 font-bold">Term {i + 1}</span>
                            </div>
                        ))}
                    </div>
                    <div className="pt-4 flex justify-between items-center text-xs text-gray-500">
                        <span>Progress track based on weighted averages</span>
                        <button className="text-brand-green font-bold hover:underline">Full Report</button>
                    </div>
                </div>

                {/* Quick Actions & Activity */}
                <div className="space-y-8">
                    <div className="card">
                        <h3 className="text-lg font-bold mb-6 text-brand-navy">Quick Actions</h3>
                        <div className="grid grid-cols-2 gap-4">
                            <button className="p-4 bg-brand-green-light text-brand-green rounded-xl font-bold hover:bg-brand-green hover:text-white transition-all text-sm border border-brand-green/20 text-left">
                                Add Student
                            </button>
                            <button className="p-4 bg-blue-50 text-blue-600 rounded-xl font-bold hover:bg-blue-600 hover:text-white transition-all text-sm border border-blue-200/50 text-left">
                                Record Attendance
                            </button>
                            <button className="p-4 bg-purple-50 text-purple-600 rounded-xl font-bold hover:bg-purple-600 hover:text-white transition-all text-sm border border-purple-200/50 text-left">
                                Create Exam
                            </button>
                            <button className="p-4 bg-amber-50 text-amber-600 rounded-xl font-bold hover:bg-amber-600 hover:text-white transition-all text-sm border border-amber-200/50 text-left">
                                Generate Report
                            </button>
                        </div>
                    </div>

                    <div className="card">
                        <h3 className="text-lg font-bold mb-4 text-brand-navy">Recent Activity</h3>
                        <div className="space-y-4">
                            {[
                                { user: "JS", name: "John Smith", action: "paid fees for Term 1", time: "2h ago" },
                                { user: "MW", name: "Mark West", action: "uploaded a new assignment", time: "5h ago" },
                            ].map((act, i) => (
                                <div key={i} className="flex items-center gap-3 pb-3 border-b border-gray-50 last:border-0 last:pb-0">
                                    <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-[10px] font-bold text-gray-500">{act.user}</div>
                                    <div>
                                        <p className="text-xs text-brand-navy"><span className="font-bold">{act.name}</span> {act.action}</p>
                                        <p className="text-[10px] text-gray-400">{act.time}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
