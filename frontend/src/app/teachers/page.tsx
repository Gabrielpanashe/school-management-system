import { Plus, Search, MoreVertical, BookOpen } from "lucide-react";

const teachers = [
    { id: "1", name: "Dr. Sarah Wilson", subject: "Mathematics", email: "sarah.w@school.com", classes: 4, status: "Active" },
    { id: "2", name: "Mr. James Bond", subject: "Physical Ed", email: "james.b@school.com", classes: 6, status: "Active" },
    { id: "3", name: "Ms. Emily Davis", subject: "English Lit", email: "emily.d@school.com", classes: 3, status: "On Leave" },
    { id: "4", name: "Dr. Robert Fox", subject: "Physics", email: "robert.f@school.com", classes: 5, status: "Active" },
];

export default function TeachersPage() {
    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-2xl font-bold text-brand-navy">Teachers</h2>
                    <p className="text-gray-500">Manage teacher profiles and subject assignments</p>
                </div>
                <button className="btn-primary flex items-center gap-2">
                    <Plus className="w-5 h-5" />
                    Add Teacher
                </button>
            </div>

            <div className="flex items-center gap-4 bg-white p-4 rounded-xl shadow-sm border border-gray-100">
                <div className="flex-1 flex items-center gap-2 px-1">
                    <Search className="w-5 h-5 text-gray-400" />
                    <input
                        type="text"
                        placeholder="Search teachers by name or subject..."
                        className="w-full bg-transparent outline-none text-sm"
                    />
                </div>
                <select className="bg-transparent text-sm font-medium outline-none border-l pl-4">
                    <option>All Subjects</option>
                    <option>Mathematics</option>
                    <option>Science</option>
                    <option>Languages</option>
                </select>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                <table className="w-full text-left">
                    <thead className="bg-gray-50 border-b">
                        <tr>
                            <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Name</th>
                            <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Department/Subject</th>
                            <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Classes</th>
                            <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Status</th>
                            <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y">
                        {teachers.map((teacher) => (
                            <tr key={teacher.id} className="hover:bg-gray-50 transition-colors">
                                <td className="px-6 py-4">
                                    <div className="flex items-center gap-3">
                                        <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-xs">
                                            {teacher.name.split(' ').map(n => n[0]).join('')}
                                        </div>
                                        <div>
                                            <span className="font-medium text-brand-navy block">{teacher.name}</span>
                                            <span className="text-xs text-gray-400">{teacher.email}</span>
                                        </div>
                                    </div>
                                </td>
                                <td className="px-6 py-4">
                                    <div className="flex items-center gap-2 text-sm text-gray-600">
                                        <BookOpen className="w-4 h-4 text-brand-green" />
                                        {teacher.subject}
                                    </div>
                                </td>
                                <td className="px-6 py-4 text-sm text-gray-600">{teacher.classes} Assign.</td>
                                <td className="px-6 py-4">
                                    <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase ${teacher.status === 'Active' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'
                                        }`}>
                                        {teacher.status}
                                    </span>
                                </td>
                                <td className="px-6 py-4">
                                    <button className="text-gray-400 hover:text-brand-navy">
                                        <MoreVertical className="w-5 h-5" />
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
