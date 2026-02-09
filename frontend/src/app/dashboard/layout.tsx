"use client";

import Link from "next/link";
import { useRouter, usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import {
    LayoutDashboard,
    Users,
    UserSquare2,
    BookOpen,
    CheckSquare,
    CreditCard,
    Settings,
    LogOut,
    Menu,
    X,
    BarChart3
} from "lucide-react";

const navItems = [
    { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    { name: "Students", href: "/students", icon: Users },
    { name: "Teachers", href: "/teachers", icon: UserSquare2 },
    { name: "Academic", href: "/academic", icon: BookOpen },
    { name: "Attendance", href: "/attendance", icon: CheckSquare },
    { name: "Performance", href: "/performance", icon: BarChart3 },
    { name: "Finance", href: "/finance", icon: CreditCard },
    { name: "Settings", href: "/settings", icon: Settings },
];

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
    const { user, loading, logout } = useAuth();
    const router = useRouter();
    const pathname = usePathname();
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);

    useEffect(() => {
        if (!loading && !user) {
            router.push("/login");
        }
    }, [user, loading, router]);

    useEffect(() => {
        setIsSidebarOpen(false); // Close sidebar on route change
    }, [pathname]);

    if (loading) return <div className="h-screen flex items-center justify-center">Loading...</div>;
    if (!user) return null;

    return (
        <div className="flex min-h-screen bg-gray-50 relative">
            {/* Mobile Sidebar Overlay */}
            {isSidebarOpen && (
                <div
                    className="fixed inset-0 bg-black/50 z-40 md:hidden"
                    onClick={() => setIsSidebarOpen(false)}
                />
            )}

            {/* Sidebar */}
            <aside className={`
        fixed inset-y-0 left-0 z-50 w-64 bg-brand-navy text-white flex-shrink-0 flex flex-col transform transition-transform duration-300 ease-in-out
        md:relative md:translate-x-0
        ${isSidebarOpen ? "translate-x-0" : "-translate-x-full"}
      `}>
                <div className="p-6 flex items-center justify-between">
                    <h2 className="text-2xl font-bold tracking-tight">SmartSchool</h2>
                    <button className="md:hidden text-white" onClick={() => setIsSidebarOpen(false)}>
                        <X className="w-6 h-6" />
                    </button>
                </div>

                <nav className="flex-1 px-4 space-y-1">
                    {navItems.map((item) => (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${pathname.startsWith(item.href)
                                ? "bg-brand-navy-dark text-white border-l-4 border-brand-green"
                                : "text-gray-300 hover:text-white hover:bg-brand-navy-dark"
                                }`}
                        >
                            <item.icon className="w-5 h-5" />
                            <span>{item.name}</span>
                        </Link>
                    ))}
                </nav>

                <div className="p-4 border-t border-blue-800">
                    <button
                        onClick={logout}
                        className="flex items-center gap-3 w-full px-4 py-3 text-gray-400 hover:text-white transition-colors"
                    >
                        <LogOut className="w-5 h-5" />
                        <span>Logout</span>
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-auto w-full">
                <header className="bg-white border-b h-16 flex items-center justify-between px-4 md:px-8 sticky top-0 z-30">
                    <div className="flex items-center gap-4">
                        <button className="md:hidden p-2 text-brand-navy" onClick={() => setIsSidebarOpen(true)}>
                            <Menu className="w-6 h-6" />
                        </button>
                        <h1 className="text-lg font-semibold text-brand-navy capitalize">
                            {pathname.split('/').pop() || 'Overview'}
                        </h1>
                    </div>

                    <div className="flex items-center gap-4">
                        <div className="text-right hidden sm:block">
                            <p className="text-sm font-medium">{user.first_name} {user.last_name}</p>
                            <p className="text-xs text-gray-500 uppercase">{user.role.replace('_', ' ')}</p>
                        </div>
                        <div className="w-10 h-10 rounded-full bg-brand-green-light flex items-center justify-center text-brand-green font-bold border border-brand-green/20">
                            {user.first_name[0]}{user.last_name[0]}
                        </div>
                    </div>
                </header>

                <div className="p-4 md:p-8">
                    {children}
                </div>
            </main>
        </div>
    );
}
