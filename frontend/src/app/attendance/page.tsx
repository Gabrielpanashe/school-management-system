"use client";

import { useState, useEffect, useCallback } from "react";
import { Check, X, Search, Calendar, Users, Loader2, AlertCircle } from "lucide-react";
import { apiFetch } from "@/lib/api";

export default function AttendancePage() {
    const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
    const [classrooms, setClassrooms] = useState<any[]>([]);
    const [selectedClassroomId, setSelectedClassroomId] = useState<string>("");
    const [students, setStudents] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [isSaving, setIsSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Fetch classrooms on mount
    useEffect(() => {
        const fetchClassrooms = async () => {
            try {
                const data = await apiFetch("/academic/classrooms");
                setClassrooms(data);
                if (data.length > 0) setSelectedClassroomId(data[0].id);
            } catch (err: any) {
                console.error("Failed to fetch classrooms", err);
            }
        };
        fetchClassrooms();
    }, []);

    // Fetch students when classroom changes
    const fetchStudents = useCallback(async () => {
        if (!selectedClassroomId) return;
        try {
            setLoading(true);
            setError(null);
            const data = await apiFetch(`/students/?classroom_id=${selectedClassroomId}`);
            // Initialize attendance status as present for all
            setStudents(data.map((s: any) => ({ ...s, status: "present" })));
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, [selectedClassroomId]);

    useEffect(() => {
        fetchStudents();
    }, [fetchStudents]);

    const toggleStatus = (id: string) => {
        setStudents(prev => prev.map(s => {
            if (s.id === id) {
                return { ...s, status: s.status === "present" ? "absent" : "present" };
            }
            return s;
        }));
    };

    const handleSave = async () => {
        if (!selectedClassroomId || students.length === 0) return;

        try {
            setIsSaving(true);
            await apiFetch("/attendance/bulk", {
                method: "POST",
                body: JSON.stringify({
                    date: date,
                    classroom_id: selectedClassroomId,
                    records: students.map(s => ({
                        student_id: s.id,
                        status: s.status,
                        remarks: ""
                    }))
                })
            });
            alert("Attendance saved successfully!");
        } catch (err: any) {
            alert("Error saving attendance: " + err.message);
        } finally {
            setIsSaving(false);
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-2xl font-bold text-brand-navy">Attendance</h2>
                    <p className="text-gray-500">Mark daily attendance for your classroom</p>
                </div>
                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2 bg-white px-4 py-2 rounded-lg border border-gray-200">
                        <Users className="w-5 h-5 text-brand-green" />
                        <select
                            className="outline-none text-sm font-medium bg-transparent"
                            value={selectedClassroomId}
                            onChange={(e) => setSelectedClassroomId(e.target.value)}
                        >
                            <option value="" disabled>Select Class</option>
                            {classrooms.map(c => (
                                <option key={c.id} value={c.id}>{c.name}</option>
                            ))}
                        </select>
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
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 space-y-4">
                    {loading ? (
                        <div className="h-64 flex flex-col items-center justify-center gap-4 bg-white rounded-xl border border-gray-100">
                            <Loader2 className="w-8 h-8 text-brand-green animate-spin" />
                            <p className="text-gray-500 font-medium">Loading class list...</p>
                        </div>
                    ) : error ? (
                        <div className="h-64 flex flex-col items-center justify-center gap-4 bg-white rounded-xl border border-red-100 text-red-600">
                            <AlertCircle className="w-8 h-8" />
                            <p className="font-bold">Error loading records</p>
                            <p className="text-sm">{error}</p>
                        </div>
                    ) : (
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
                                    {students.length === 0 ? (
                                        <tr>
                                            <td colSpan={3} className="px-6 py-12 text-center text-gray-500">
                                                No students found in this classroom.
                                            </td>
                                        </tr>
                                    ) : (
                                        students.map((student) => (
                                            <tr key={student.id} className="hover:bg-gray-50 transition-colors">
                                                <td className="px-6 py-4">
                                                    <div className="flex items-center gap-3">
                                                        <div className="w-8 h-8 rounded-full bg-brand-green-light flex items-center justify-center text-brand-green font-bold text-xs uppercase">
                                                            {student.first_name[0]}{student.last_name[0]}
                                                        </div>
                                                        <span className="font-medium text-brand-navy">{student.first_name} {student.last_name}</span>
                                                    </div>
                                                </td>
                                                <td className="px-6 py-4 text-sm text-gray-600 font-mono">{student.admission_number}</td>
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
                                        ))
                                    )}
                                </tbody>
                            </table>
                        </div>
                    )}
                    <div className="flex justify-end">
                        <button
                            onClick={handleSave}
                            disabled={isSaving || students.length === 0}
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
                                <span className="font-bold text-green-600">{students.filter(s => s.status === 'present').length}</span>
                            </div>
                            <div className="flex justify-between items-center pb-2 border-b">
                                <span className="text-sm text-gray-500">Absent</span>
                                <span className="font-bold text-red-600">{students.filter(s => s.status === 'absent').length}</span>
                            </div>
                            <div className="flex justify-between items-center">
                                <span className="text-sm text-gray-500">Attendance Rate</span>
                                <span className="font-bold text-brand-navy">
                                    {students.length > 0 ? Math.round((students.filter(s => s.status === 'present').length / students.length) * 100) : 0}%
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
