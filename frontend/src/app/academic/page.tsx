"use client";

import { useState } from "react";
import { Plus, Calendar, Book, Layers, MoreHorizontal, Users } from "lucide-react";

export default function AcademicPage() {
    const [activeTab, setActiveTab] = useState("years");

    const tabs = [
        { id: "years", name: "Academic Years", icon: Calendar },
        { id: "terms", name: "Terms", icon: Layers },
        { id: "subjects", name: "Subjects", icon: Book },
        { id: "classrooms", name: "Classrooms", icon: Users },
    ];

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-2xl font-bold text-brand-navy">Academic Setup</h2>
                    <p className="text-gray-500">Configure your school's curriculum and calendar</p>
                </div>
                <button className="btn-primary flex items-center gap-2">
                    <Plus className="w-5 h-5" />
                    Add {activeTab.slice(0, -1)}
                </button>
            </div>

            {/* Tabs */}
            <div className="flex gap-2 border-b">
                {tabs.map((tab) => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`flex items-center gap-2 px-6 py-3 text-sm font-semibold transition-all border-b-2 ${activeTab === tab.id
                            ? "border-brand-green text-brand-green bg-brand-green-light/30"
                            : "border-transparent text-gray-400 hover:text-gray-600 hover:bg-gray-50"
                            }`}
                    >
                        <tab.icon className="w-4 h-4" />
                        {tab.name}
                    </button>
                ))}
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
                {activeTab === 'years' && (
                    <div className="space-y-4">
                        <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-100">
                            <div>
                                <h4 className="font-bold text-brand-navy">Academic Year 2026</h4>
                                <p className="text-xs text-gray-500">Jan 1, 2026 - Dec 31, 2026</p>
                            </div>
                            <div className="flex items-center gap-3">
                                <span className="bg-green-100 text-green-700 px-2 py-1 rounded text-[10px] uppercase font-bold">Current</span>
                                <button className="text-gray-400 hover:text-brand-navy"><MoreHorizontal className="w-5 h-5" /></button>
                            </div>
                        </div>
                        <div className="flex items-center justify-between p-4 bg-white rounded-lg border border-gray-100">
                            <div>
                                <h4 className="font-bold text-gray-400">Academic Year 2025</h4>
                                <p className="text-xs text-gray-400">Jan 1, 2025 - Dec 31, 2025</p>
                            </div>
                            <div className="flex items-center gap-3">
                                <span className="bg-gray-100 text-gray-500 px-2 py-1 rounded text-[10px] uppercase font-bold">Completed</span>
                                <button className="text-gray-400 hover:text-brand-navy"><MoreHorizontal className="w-5 h-5" /></button>
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === 'terms' && (
                    <div className="space-y-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="card hover:border-brand-green cursor-pointer">
                                <h4 className="font-bold text-brand-navy">Term 1 (Lent)</h4>
                                <p className="text-sm text-gray-500 mb-4 font-medium">Status: Active</p>
                                <div className="w-full bg-gray-100 h-1.5 rounded-full overflow-hidden">
                                    <div className="bg-brand-green h-full" style={{ width: '45%' }}></div>
                                </div>
                                <p className="text-[10px] text-gray-400 mt-2">45% of term elapsed</p>
                            </div>
                            <div className="card opacity-60">
                                <h4 className="font-bold text-brand-navy">Term 2 (Trinity)</h4>
                                <p className="text-sm text-gray-500 mb-4 font-medium">Status: Scheduled</p>
                                <div className="w-full bg-gray-100 h-1.5 rounded-full"></div>
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === 'subjects' && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                        {['Mathematics', 'Physics', 'English', 'History', 'Geography', 'Art', 'Biology'].map(sub => (
                            <div key={sub} className="p-4 bg-gray-50 rounded-xl border border-gray-100 flex items-center justify-between">
                                <span className="font-semibold text-sm text-brand-navy">{sub}</span>
                                <button className="text-gray-300 hover:text-red-500"><Plus className="w-4 h-4 rotate-45" /></button>
                            </div>
                        ))}
                    </div>
                )}

                {activeTab === 'classrooms' && (
                    <div className="space-y-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {[
                                { name: "Grade 10-A", level: "Grade 10", room: "R101", students: 32 },
                                { name: "Grade 10-B", level: "Grade 10", room: "R102", students: 28 },
                                { name: "Grade 11-A", level: "Grade 11", room: "R201", students: 35 },
                                { name: "Grade 12-Science", level: "Grade 12", room: "Lab-1", students: 24 },
                            ].map((cls) => (
                                <div key={cls.name} className="card hover:border-brand-green group cursor-pointer transition-all">
                                    <div className="flex justify-between items-start mb-4">
                                        <div className="bg-brand-green-light text-brand-green p-2 rounded-lg group-hover:bg-brand-green group-hover:text-white transition-colors">
                                            <Layers className="w-5 h-5" />
                                        </div>
                                        <button className="text-gray-400 hover:text-brand-navy">
                                            <MoreHorizontal className="w-5 h-5" />
                                        </button>
                                    </div>
                                    <h4 className="font-bold text-brand-navy text-lg mb-1">{cls.name}</h4>
                                    <p className="text-sm text-gray-500 mb-4">{cls.level}</p>

                                    <div className="flex items-center justify-between pt-4 border-t border-gray-50 text-xs">
                                        <div className="flex items-center gap-2">
                                            <Users className="w-4 h-4 text-gray-400" />
                                            <span className="font-bold text-brand-navy">{cls.students} Students</span>
                                        </div>
                                        <div className="bg-gray-50 px-2 py-1 rounded text-gray-600 font-medium">
                                            Room: {cls.room}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
