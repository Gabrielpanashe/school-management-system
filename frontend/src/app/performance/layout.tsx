"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";
import { BarChart3, FileText, LayoutList } from "lucide-react";

export default function PerformanceLayout({ children }: { children: React.ReactNode }) {
    const pathname = usePathname();

    const tabs = [
        { name: "Grades & Assessments", href: "/performance/grades", icon: LayoutList },
        { name: "Report Cards", href: "/performance/report-cards", icon: FileText },
    ];

    return (
        <div className="space-y-6">
            <div className="flex gap-2 border-b overflow-x-auto">
                {tabs.map((tab) => (
                    <Link
                        key={tab.href}
                        href={tab.href}
                        className={`flex items-center gap-2 px-6 py-3 text-sm font-semibold transition-all border-b-2 whitespace-nowrap ${pathname === tab.href
                            ? "border-brand-green text-brand-green bg-brand-green-light/30"
                            : "border-transparent text-gray-400 hover:text-gray-600 hover:bg-gray-50"
                            }`}
                    >
                        <tab.icon className="w-4 h-4" />
                        {tab.name}
                    </Link>
                ))}
            </div>
            <div>{children}</div>
        </div>
    );
}
