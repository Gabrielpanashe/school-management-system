"use client";

import { useState } from "react";
import { Plus, Search, Edit3, Trash2, BookOpen } from "lucide-react";

const mockAssessments = [
    { id: "1", title: "Mid-Term Exam", type: "Exam", subject: "Mathematics", weight: 30, total: 100 },
    { id: "2", title: "Weekly Quiz", type: "Quiz", subject: "Science", weight: 10, total: 20 },
    { id: "3", title: "Project Alpha", type: "Assignment", subject: "History", weight: 20, total: 50 },
];

export default function PerformanceGradesPage() {
    const [assessments] = useState(mockAssessments);

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-2xl font-bold text-brand-navy">Assessments & Grades</h2>
                    <p className="text-gray-500">Manage student evaluations and grade distributions</p>
                </div>
                <button className="btn-primary flex items-center gap-2">
                    <Plus className="w-5 h-5" />
                    New Assessment
                </button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                <div className="lg:col-span-1 space-y-4">
                    <div className="card bg-brand-navy text-white">
                        <h3 className="font-bold mb-2">Grading Tip</h3>
                        <p className="text-sm text-blue-100 italic">
                            "Total weight for a term should aim for 100% for accurate final averages."
                        </p>
                    </div>

                    <div className="card">
                        <h3 className="font-bold text-brand-navy mb-4">Filters</h3>
                        <div className="space-y-3">
                            <label className="block text-xs font-bold uppercase text-gray-400">Term</label>
                            <select className="w-full bg-gray-50 border border-gray-100 rounded-lg px-3 py-2 text-sm outline-none">
                                <option>First Term 2026</option>
                                <option>Second Term 2026</option>
                            </select>

                            <label className="block text-xs font-bold uppercase text-gray-400 mt-4">Class</label>
                            <select className="w-full bg-gray-50 border border-gray-100 rounded-lg px-3 py-2 text-sm outline-none">
                                <option>Grade 10-A</option>
                                <option>Grade 10-B</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div className="lg:col-span-3 space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                        {assessments.map((asm) => (
                            <div key={asm.id} className="card group cursor-pointer hover:border-brand-green">
                                <div className="flex justify-between items-start mb-4">
                                    <div className="bg-brand-green-light text-brand-green p-2 rounded-lg">
                                        <BookOpen className="w-5 h-5" />
                                    </div>
                                    <span className="text-[10px] font-bold uppercase bg-gray-100 px-2 py-1 rounded text-gray-500">
                                        {asm.type}
                                    </span>
                                </div>
                                <h4 className="font-bold text-brand-navy mb-1 group-hover:text-brand-green transition-colors">
                                    {asm.title}
                                </h4>
                                <p className="text-sm text-gray-500 mb-4">{asm.subject}</p>

                                <div className="flex items-center justify-between pt-4 border-t border-gray-50 text-xs">
                                    <div>
                                        <span className="text-gray-400">Weight: </span>
                                        <span className="font-bold text-brand-navy">{asm.weight}%</span>
                                    </div>
                                    <div>
                                        <span className="text-gray-400">Total: </span>
                                        <span className="font-bold text-brand-navy">{asm.total}mks</span>
                                    </div>
                                </div>

                                <div className="flex gap-2 mt-4">
                                    <button className="flex-1 bg-gray-50 text-gray-600 py-2 rounded-lg text-xs font-bold hover:bg-brand-green hover:text-white transition-all">
                                        Enter Grades
                                    </button>
                                    <button className="p-2 bg-gray-50 text-gray-400 rounded-lg hover:text-red-500 transition-colors">
                                        <Trash2 className="w-4 h-4" />
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
