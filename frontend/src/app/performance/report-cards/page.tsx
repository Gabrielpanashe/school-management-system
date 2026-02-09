"use client";

import { useState } from "react";
import { Search, Download, FileText, User, Filter, ChevronRight } from "lucide-react";

const mockReportCards = [
    { id: "1", student: "Alice Johnson", admission: "ADM-001", class: "Grade 10-A", average: 88.5, status: "Finalized" },
    { id: "2", student: "Bob Smith", admission: "ADM-002", class: "Grade 10-A", average: 72.4, status: "Draft" },
    { id: "3", student: "Diana Prince", admission: "ADM-004", class: "Grade 10-B", average: 94.1, status: "Finalized" },
];

export default function ReportCardsPage() {
    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-2xl font-bold text-brand-navy">Report Cards</h2>
                    <p className="text-gray-500">Generate and distribute termly student performance summaries</p>
                </div>
                <div className="flex gap-2">
                    <button className="bg-white border text-gray-600 px-4 py-2 rounded-lg font-semibold hover:bg-gray-50 flex items-center gap-2">
                        <Download className="w-4 h-4" />
                        Bulk Export
                    </button>
                    <button className="btn-primary">Generate All</button>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                <div className="lg:col-span-1">
                    <div className="card space-y-4">
                        <h3 className="font-bold text-brand-navy">Filter Reports</h3>
                        <div className="space-y-4">
                            <div>
                                <label className="block text-xs font-bold uppercase text-gray-400 mb-2">Class</label>
                                <select className="w-full bg-gray-50 border border-gray-100 rounded-lg px-3 py-2 text-sm outline-none">
                                    <option>Grade 10-A</option>
                                    <option>Grade 10-B</option>
                                </select>
                            </div>
                            <div>
                                <label className="block text-xs font-bold uppercase text-gray-400 mb-2">Academic Term</label>
                                <select className="w-full bg-gray-50 border border-gray-100 rounded-lg px-3 py-2 text-sm outline-none">
                                    <option>Term 1 (Lent) 2026</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="lg:col-span-3 space-y-4">
                    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                        <table className="w-full text-left">
                            <thead className="bg-gray-50 border-b">
                                <tr>
                                    <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Student</th>
                                    <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Class</th>
                                    <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Avg %</th>
                                    <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Status</th>
                                    <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Action</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y">
                                {mockReportCards.map((rc) => (
                                    <tr key={rc.id} className="hover:bg-gray-50 group transition-colors">
                                        <td className="px-6 py-4">
                                            <div className="flex items-center gap-3">
                                                <div className="w-8 h-8 rounded-full bg-brand-green-light flex items-center justify-center text-brand-green font-bold text-xs">
                                                    {rc.student.split(' ').map(n => n[0]).join('')}
                                                </div>
                                                <div>
                                                    <p className="font-medium text-brand-navy">{rc.student}</p>
                                                    <p className="text-[10px] text-gray-400">{rc.admission}</p>
                                                </div>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 text-sm text-gray-600">{rc.class}</td>
                                        <td className="px-6 py-4">
                                            <span className={`font-bold ${rc.average >= 80 ? 'text-green-600' : 'text-amber-600'}`}>
                                                {rc.average}%
                                            </span>
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className={`px-2 py-1 rounded-full text-[10px] font-bold uppercase ${rc.status === 'Finalized' ? 'bg-green-50 text-green-700' : 'bg-gray-100 text-gray-500'
                                                }`}>
                                                {rc.status}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4">
                                            <button className="flex items-center gap-1 text-brand-navy hover:text-brand-green font-semibold text-sm">
                                                <FileText className="w-4 h-4" />
                                                View
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
}
