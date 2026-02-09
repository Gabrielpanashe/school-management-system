"use client";

import { useState, useEffect } from "react";
import { Check, X, Search, Calendar } from "lucide-react";
import { apiFetch } from "@/lib/api";

const mockStudents = [
    { id: "1", name: "Alice Johnson", admission: "ADM-001", status: "present" },
    { id: "2", name: "Bob Smith", admission: "ADM-002", status: "present" },
    { id: "3", name: "Charlie Brown", admission: "ADM-003", status: "absent" },
    { id: "4", name: "Diana Prince", admission: "ADM-004", status: "present" },
];

export default function AttendancePage() {
    const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
    const [attendance, setAttendance] = useState<any[]>(mockStudents);
    const [isSaving, setIsSaving] = useState(false);

    const toggleStatus = (id: string) => {
        setAttendance(prev => prev.map(s => {
            if (s.id === id) {
                return { ...s, status: s.status === "present" ? "absent" : "present" };
            }
            return s;
        }));
    };

    const handleSave = async () => {
        setIsSaving(true);
        // Logic to save to backend...
        setTimeout(() => setIsSaving(false), 1000);
    };

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-2xl font-bold text-brand-navy">Attendance</h2>
                    <p className="text-gray-500">Mark daily attendance for your classroom</p>
                </div>
                <div className="flex items-center gap-2 bg-white px-4 py-2 rounded-lg border border-gray-200">
                    <Calendar className="w-5 h-5 text-brand-green" />
                    <input
                        type="date"
                        className="outline-none text-sm font-medium"
                        value={date}
                        onChange={(e) => setDate(e.target.value)}
                    />
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 space-y-4">
                    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                        <table className="w-full text-left">
                            <thead className="bg-gray-50 border-b">
                                <tr>
                                    <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Student</th>
                                    <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Admission</th>
                                    <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500 text-center">Status</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y">
                                {attendance.map((student) => (
                                    <tr key={student.id} className="hover:bg-gray-50 transition-colors">
                                        <td className="px-6 py-4">
                                            <div className="flex items-center gap-3">
                                                <div className="w-8 h-8 rounded-full bg-brand-green-light flex items-center justify-center text-brand-green font-bold text-xs">
                                                    {student.name.split(' ').map((n: any) => n[0]).join('')}
                                                </div>
                                                <span className="font-medium text-brand-navy">{student.name}</span>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 text-sm text-gray-600">{student.admission}</td>
                                        <td className="px-6 py-4">
                                            <div className="flex justify-center gap-2">
                                                <button
                                                    onClick={() => toggleStatus(student.id)}
                                                    className={`w-10 h-10 rounded-lg flex items-center justify-center transition-all ${student.status === "present"
                                                            ? "bg-green-500 text-white shadow-md"
                                                            : "bg-gray-100 text-gray-400 hover:bg-gray-200"
                                                        }`}
                                                >
                                                    <Check className="w-5 h-5" />
                                                </button>
                                                <button
                                                    onClick={() => toggleStatus(student.id)}
                                                    className={`w-10 h-10 rounded-lg flex items-center justify-center transition-all ${student.status === "absent"
                                                            ? "bg-red-500 text-white shadow-md"
                                                            : "bg-gray-100 text-gray-400 hover:bg-gray-200"
                                                        }`}
                                                >
                                                    <X className="w-5 h-5" />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                    <div className="flex justify-end">
                        <button
                            onClick={handleSave}
                            disabled={isSaving}
                            className="btn-primary px-8 disabled:opacity-50"
                        >
                            {isSaving ? "Saving..." : "Save Attendance"}
                        </button>
                    </div>
                </div>

                <div className="space-y-6">
                    <div className="card">
                        <h3 className="text-lg font-bold mb-4 text-brand-navy">Summary</h3>
                        <div className="space-y-4">
                            <div className="flex justify-between items-center pb-2 border-b">
                                <span className="text-sm text-gray-500">Present</span>
                                <span className="font-bold text-green-600">{attendance.filter(s => s.status === 'present').length}</span>
                            </div>
                            <div className="flex justify-between items-center pb-2 border-b">
                                <span className="text-sm text-gray-500">Absent</span>
                                <span className="font-bold text-red-600">{attendance.filter(s => s.status === 'absent').length}</span>
                            </div>
                            <div className="flex justify-between items-center">
                                <span className="text-sm text-gray-500">Attendance Rate</span>
                                <span className="font-bold text-brand-navy">
                                    {Math.round((attendance.filter(s => s.status === 'present').length / attendance.length) * 100)}%
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
