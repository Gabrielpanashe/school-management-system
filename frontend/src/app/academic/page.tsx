"use client";

import { useEffect, useState, useCallback } from "react";
import { Plus, Calendar, Book, Layers, MoreHorizontal, Users, Loader2 } from "lucide-react";
import { apiFetch } from "@/lib/api";

export default function AcademicPage() {
    const [activeTab, setActiveTab] = useState("years");
    const [data, setData] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedYearId, setSelectedYearId] = useState<string | null>(null);

    const tabs = [
        { id: "years", name: "Academic Years", icon: Calendar },
        { id: "terms", name: "Terms", icon: Layers },
        { id: "subjects", name: "Subjects", icon: Book },
        { id: "classrooms", name: "Classrooms", icon: Users },
    ];

    const fetchData = useCallback(async () => {
        try {
            setLoading(true);
            setError(null);
            let endpoint = "";

            if (activeTab === "years") endpoint = "/academic/years";
            else if (activeTab === "terms") {
                if (!selectedYearId) {
                    // Try to fetch years first to get a year_id if not selected
                    const years = await apiFetch("/academic/years");
                    if (years.length > 0) {
                        const currentYear = years.find((y: any) => y.status === 'active') || years[0];
                        setSelectedYearId(currentYear.id);
                        endpoint = `/academic/terms?year_id=${currentYear.id}`;
                    } else {
                        setData([]);
                        setLoading(false);
                        return;
                    }
                } else {
                    endpoint = `/academic/terms?year_id=${selectedYearId}`;
                }
            }
            else if (activeTab === "subjects") endpoint = "/subjects/";
            else if (activeTab === "classrooms") endpoint = "/academic/classrooms";

            const result = await apiFetch(endpoint);
            setData(result);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, [activeTab, selectedYearId]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

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

            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 min-h-[300px] flex flex-col">
                {loading ? (
                    <div className="flex-1 flex flex-col items-center justify-center gap-4">
                        <Loader2 className="w-8 h-8 text-brand-green animate-spin" />
                        <p className="text-gray-500 text-sm font-medium">Fetching {activeTab}...</p>
                    </div>
                ) : error ? (
                    <div className="flex-1 flex flex-col items-center justify-center gap-4 text-red-600">
                        <p className="font-bold">Failed to load {activeTab}</p>
                        <p className="text-sm">{error}</p>
                        <button onClick={fetchData} className="text-brand-navy underline text-xs font-semibold">Try Again</button>
                    </div>
                ) : (
                    <>
                        {activeTab === 'years' && (
                            <div className="space-y-4">
                                {data.length === 0 ? (
                                    <p className="text-center text-gray-500 py-12">No academic years configured.</p>
                                ) : (
                                    data.map((year) => (
                                        <div key={year.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-100">
                                            <div>
                                                <h4 className="font-bold text-brand-navy">{year.name}</h4>
                                                <p className="text-xs text-gray-500">
                                                    {new Date(year.start_date).toLocaleDateString()} - {new Date(year.end_date).toLocaleDateString()}
                                                </p>
                                            </div>
                                            <div className="flex items-center gap-3">
                                                {year.is_active && <span className="bg-green-100 text-green-700 px-2 py-1 rounded text-[10px] uppercase font-bold">Current</span>}
                                                <button className="text-gray-400 hover:text-brand-navy"><MoreHorizontal className="w-5 h-5" /></button>
                                            </div>
                                        </div>
                                    ))
                                )}
                            </div>
                        )}

                        {activeTab === 'terms' && (
                            <div className="space-y-4">
                                {data.length === 0 ? (
                                    <p className="text-center text-gray-500 py-12">No terms found for this year.</p>
                                ) : (
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        {data.map((term) => (
                                            <div key={term.id} className="card hover:border-brand-green cursor-pointer">
                                                <h4 className="font-bold text-brand-navy">{term.name}</h4>
                                                <p className="text-sm text-gray-500 mb-2">
                                                    {new Date(term.start_date).toLocaleDateString()} to {new Date(term.end_date).toLocaleDateString()}
                                                </p>
                                                <span className={`text-[10px] font-bold uppercase px-2 py-1 rounded ${term.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'}`}>
                                                    {term.is_active ? 'Active' : 'Closed'}
                                                </span>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        )}

                        {activeTab === 'subjects' && (
                            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                                {data.length === 0 ? (
                                    <p className="col-span-full text-center text-gray-500 py-12">No subjects defined yet.</p>
                                ) : (
                                    data.map(sub => (
                                        <div key={sub.id} className="p-4 bg-gray-50 rounded-xl border border-gray-100 flex items-center justify-between">
                                            <div className="flex flex-col">
                                                <span className="font-semibold text-sm text-brand-navy">{sub.name}</span>
                                                <span className="text-[10px] text-gray-400 font-mono">{sub.code}</span>
                                            </div>
                                            <button className="text-gray-300 hover:text-red-500"><Plus className="w-4 h-4 rotate-45" /></button>
                                        </div>
                                    ))
                                )}
                            </div>
                        )}

                        {activeTab === 'classrooms' && (
                            <div className="space-y-4">
                                {data.length === 0 ? (
                                    <p className="text-center text-gray-500 py-12">No classrooms setup yet.</p>
                                ) : (
                                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                        {data.map((cls) => (
                                            <div key={cls.id} className="card hover:border-brand-green group cursor-pointer transition-all">
                                                <div className="flex justify-between items-start mb-4">
                                                    <div className="bg-brand-green-light text-brand-green p-2 rounded-lg group-hover:bg-brand-green group-hover:text-white transition-colors">
                                                        <Layers className="w-5 h-5" />
                                                    </div>
                                                    <button className="text-gray-400 hover:text-brand-navy">
                                                        <MoreHorizontal className="w-5 h-5" />
                                                    </button>
                                                </div>
                                                <h4 className="font-bold text-brand-navy text-lg mb-1">{cls.name}</h4>
                                                <p className="text-sm text-gray-500 mb-4">{cls.level || "Grade Level"}</p>

                                                <div className="flex items-center justify-between pt-4 border-t border-gray-50 text-xs">
                                                    <div className="flex items-center gap-2">
                                                        <Users className="w-4 h-4 text-gray-400" />
                                                        <span className="font-bold text-brand-navy">{cls.capacity || 0} Capacity</span>
                                                    </div>
                                                    <div className="bg-gray-50 px-2 py-1 rounded text-gray-600 font-medium font-mono">
                                                        ID: {cls.id.slice(0, 8)}
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
}
