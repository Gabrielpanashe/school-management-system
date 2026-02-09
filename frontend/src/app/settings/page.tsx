"use client";

import { useState } from "react";
import {
    School,
    User,
    Bell,
    Shield,
    Save,
    Globe,
    Mail,
    Phone,
    MapPin
} from "lucide-react";

export default function SettingsPage() {
    const [activeSection, setActiveSection] = useState("school");

    const sections = [
        { id: "school", name: "School Profile", icon: School },
        { id: "account", name: "Account Info", icon: User },
        { id: "notifications", name: "Notifications", icon: Bell },
        { id: "privacy", name: "Security & Privacy", icon: Shield },
    ];

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-2xl font-bold text-brand-navy">Settings</h2>
                <p className="text-gray-500">Manage your school profile and system preferences</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
                {/* Sidebar Navigation */}
                <div className="lg:col-span-1 space-y-1">
                    {sections.map((s) => (
                        <button
                            key={s.id}
                            onClick={() => setActiveSection(s.id)}
                            className={`flex items-center gap-3 w-full px-4 py-3 rounded-xl text-sm font-semibold transition-all ${activeSection === s.id
                                    ? "bg-brand-navy text-white shadow-md"
                                    : "text-gray-500 hover:bg-gray-100"
                                }`}
                        >
                            <s.icon className="w-5 h-5" />
                            {s.name}
                        </button>
                    ))}
                </div>

                {/* Main Settings Content */}
                <div className="lg:col-span-3">
                    <div className="card space-y-8">
                        {activeSection === "school" && (
                            <div className="animate-in fade-in slide-in-from-bottom-2 duration-300">
                                <h3 className="text-lg font-bold text-brand-navy border-b pb-4 mb-6">School Profile</h3>

                                <div className="space-y-6">
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-2">School Name</label>
                                            <div className="relative">
                                                <School className="w-4 h-4 absolute left-3 top-3 text-gray-400" />
                                                <input
                                                    type="text"
                                                    defaultValue="Antigravity International School"
                                                    className="pl-10 w-full bg-gray-50 border border-gray-100 rounded-lg px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-brand-green"
                                                />
                                            </div>
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-2">Registration ID</label>
                                            <input
                                                type="text"
                                                defaultValue="REG-2026-X8"
                                                className="w-full bg-gray-50 border border-gray-100 rounded-lg px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-brand-green"
                                            />
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
                                            <div className="relative">
                                                <Mail className="w-4 h-4 absolute left-3 top-3 text-gray-400" />
                                                <input
                                                    type="email"
                                                    defaultValue="admin@antigravity.edu"
                                                    className="pl-10 w-full bg-gray-50 border border-gray-100 rounded-lg px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-brand-green"
                                                />
                                            </div>
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-2">Phone Number</label>
                                            <div className="relative">
                                                <Phone className="w-4 h-4 absolute left-3 top-3 text-gray-400" />
                                                <input
                                                    type="text"
                                                    defaultValue="+263 77 123 4567"
                                                    className="pl-10 w-full bg-gray-50 border border-gray-100 rounded-lg px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-brand-green"
                                                />
                                            </div>
                                        </div>
                                    </div>

                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-2">Physical Address</label>
                                        <div className="relative">
                                            <MapPin className="w-4 h-4 absolute left-3 top-3 text-gray-400" />
                                            <textarea
                                                rows={3}
                                                defaultValue="123 Innovation Drive, Tech District, Harare, Zimbabwe"
                                                className="pl-10 w-full bg-gray-50 border border-gray-100 rounded-lg px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-brand-green"
                                            />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}

                        {activeSection === "account" && (
                            <div className="animate-in fade-in slide-in-from-bottom-2 duration-300">
                                <h3 className="text-lg font-bold text-brand-navy border-b pb-4 mb-6">User Profile</h3>
                                <p className="text-sm text-gray-500 italic pb-6">Your personal contact information and preferences.</p>
                                {/* Similar form fields for user account */}
                                <div className="p-12 bg-gray-50 rounded-xl border-2 border-dashed border-gray-100 flex items-center justify-center text-gray-400">
                                    Account fields coming soon...
                                </div>
                            </div>
                        )}

                        <div className="pt-8 border-t flex justify-end">
                            <button className="btn-primary flex items-center gap-2 px-8">
                                <Save className="w-5 h-5" />
                                Save Changes
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
