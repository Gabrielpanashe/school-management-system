"use client";

import { useEffect, useState } from "react";
import { Plus, Search, MoreVertical, BookOpen, Loader2 } from "lucide-react";
import { apiFetch } from "@/lib/api";

export default function TeachersPage() {
    const [teachers, setTeachers] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchTeachers = async () => {
            try {
                setLoading(true);
                // Fetch users with the "teacher" role
                const data = await apiFetch("/users/?role=teacher");
                setTeachers(data);
                setError(null);
            } catch (err: any) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchTeachers();
    }, []);

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-2xl font-bold text-brand-navy">Teachers</h2>
                    <p className="text-gray-500">Manage teacher profiles and subject assignments</p>
                </div>
                <button className="btn-primary flex items-center gap-2">
                    <Plus className="w-5 h-5" />
                    Add Teacher
                </button>
            </div>

            <div className="flex items-center gap-4 bg-white p-4 rounded-xl shadow-sm border border-gray-100">
                <div className="flex-1 flex items-center gap-2 px-1">
                    <Search className="w-5 h-5 text-gray-400" />
                    <input
                        type="text"
                        placeholder="Search teachers by name or subject..."
                        className="w-full bg-transparent outline-none text-sm"
                    />
                </div>
                <select className="bg-transparent text-sm font-medium outline-none border-l pl-4">
                    <option>All Subjects</option>
                    <option>Mathematics</option>
                    <option>Science</option>
                    <option>Languages</option>
                </select>
            </div>

            {loading ? (
                <div className="h-64 flex flex-col items-center justify-center gap-4 bg-white rounded-xl border border-gray-100">
                    <Loader2 className="w-8 h-8 text-brand-green animate-spin" />
                    <p className="text-gray-500 font-medium">Loading teachers...</p>
                </div>
            ) : error ? (
                <div className="h-64 flex flex-col items-center justify-center gap-4 bg-white rounded-xl border border-red-100 text-red-600">
                    <p className="font-bold text-lg">Error loading records</p>
                    <p className="text-sm">{error}</p>
                </div>
            ) : (
                <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                    <table className="w-full text-left">
                        <thead className="bg-gray-50 border-b">
                            <tr>
                                <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Name</th>
                                <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Department/Subject</th>
                                <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Last Login</th>
                                <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Status</th>
                                <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y">
                            {teachers.length === 0 ? (
                                <tr>
                                    <td colSpan={5} className="px-6 py-12 text-center text-gray-500">
                                        No teachers found. Invite your first teacher to get started.
                                    </td>
                                </tr>
                            ) : (
                                teachers.map((teacher) => (
                                    <tr key={teacher.id} className="hover:bg-gray-50 transition-colors">
                                        <td className="px-6 py-4">
                                            <div className="flex items-center gap-3">
                                                <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-xs uppercase">
                                                    {teacher.first_name[0]}{teacher.last_name[0]}
                                                </div>
                                                <div>
                                                    <span className="font-medium text-brand-navy block">{teacher.first_name} {teacher.last_name}</span>
                                                    <span className="text-xs text-gray-400">{teacher.email}</span>
                                                </div>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <div className="flex items-center gap-2 text-sm text-gray-600">
                                                <BookOpen className="w-4 h-4 text-brand-green" />
                                                {teacher.department || "General"}
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 text-sm text-gray-600">
                                            {teacher.last_login ? new Date(teacher.last_login).toLocaleDateString() : "Never"}
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase ${teacher.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                                                }`}>
                                                {teacher.is_active ? 'Active' : 'Inactive'}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4">
                                            <button className="text-gray-400 hover:text-brand-navy">
                                                <MoreVertical className="w-5 h-5" />
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}
