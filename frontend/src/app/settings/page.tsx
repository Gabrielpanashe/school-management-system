"use client";

import { useEffect, useState } from "react";
import {
    School,
    User,
    Bell,
    Shield,
    Save,
    Mail,
    Phone,
    MapPin,
    Loader2,
    CheckCircle2
} from "lucide-react";
import { apiFetch } from "@/lib/api";

export default function SettingsPage() {
    const [activeSection, setActiveSection] = useState("school");
    const [school, setSchool] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState(false);

    const sections = [
        { id: "school", name: "School Profile", icon: School },
        { id: "account", name: "Account Info", icon: User },
        { id: "notifications", name: "Notifications", icon: Bell },
        { id: "privacy", name: "Security & Privacy", icon: Shield },
    ];

    useEffect(() => {
        const fetchSchool = async () => {
            try {
                setLoading(true);
                // First get current user to find school_id
                const user = await apiFetch("/auth/me");
                if (user.school_id) {
                    const schoolData = await apiFetch(`/schools/${user.school_id}`);
                    setSchool(schoolData);
                }
            } catch (err: any) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        fetchSchool();
    }, []);

    const handleSave = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!school) return;

        try {
            setSaving(true);
            setSuccess(false);
            const formData = new FormData(e.target as HTMLFormElement);
            const updateData = {
                name: formData.get("name"),
                email: formData.get("email"),
                phone: formData.get("phone"),
                address: formData.get("address"),
            };

            await apiFetch(`/schools/${school.id}`, {
                method: "PATCH",
                body: JSON.stringify(updateData)
            });

            setSuccess(true);
            setTimeout(() => setSuccess(false), 3000);
        } catch (err: any) {
            alert("Error saving settings: " + err.message);
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return (
            <div className="h-64 flex flex-col items-center justify-center gap-4 bg-white rounded-xl border border-gray-100">
                <Loader2 className="w-8 h-8 text-brand-green animate-spin" />
                <p className="text-gray-500 font-medium">Loading settings...</p>
            </div>
        );
    }

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
                    <form onSubmit={handleSave} className="card space-y-8">
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
                                                    name="name"
                                                    defaultValue={school?.name}
                                                    className="pl-10 w-full bg-gray-50 border border-gray-100 rounded-lg px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-brand-green"
                                                />
                                            </div>
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-2">Registration ID</label>
                                            <input
                                                type="text"
                                                disabled
                                                defaultValue={school?.id.slice(0, 8).toUpperCase()}
                                                className="w-full bg-gray-100 border border-gray-100 rounded-lg px-3 py-2 text-sm outline-none cursor-not-allowed"
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
                                                    name="email"
                                                    defaultValue={school?.email}
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
                                                    name="phone"
                                                    defaultValue={school?.phone}
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
                                                name="address"
                                                defaultValue={school?.address}
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
                                <div className="p-12 bg-gray-50 rounded-xl border-2 border-dashed border-gray-100 flex items-center justify-center text-gray-400">
                                    Account fields coming soon...
                                </div>
                            </div>
                        )}

                        <div className="pt-8 border-t flex justify-end items-center gap-4">
                            {success && (
                                <span className="text-green-600 text-sm font-bold flex items-center gap-2">
                                    <CheckCircle2 className="w-4 h-4" />
                                    Settings saved!
                                </span>
                            )}
                            <button
                                type="submit"
                                disabled={saving}
                                className="btn-primary flex items-center gap-2 px-8 disabled:opacity-50"
                            >
                                {saving ? <Loader2 className="w-5 h-5 animate-spin" /> : <Save className="w-5 h-5" />}
                                {saving ? "Saving..." : "Save Changes"}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}
