import { Plus, Search, MoreVertical } from "lucide-react";

const students = [
    { id: "1", name: "Alice Johnson", admission: "ADM-001", class: "Grade 10-A", gender: "Female", status: "Active" },
    { id: "2", name: "Bob Smith", admission: "ADM-002", class: "Grade 10-B", gender: "Male", status: "Active" },
    { id: "3", name: "Charlie Brown", admission: "ADM-003", class: "Grade 9-A", gender: "Male", status: "Inactive" },
    { id: "4", name: "Diana Prince", admission: "ADM-004", class: "Grade 12-C", gender: "Female", status: "Active" },
];

export default function StudentsPage() {
    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-2xl font-bold text-brand-navy">Students</h2>
                    <p className="text-gray-500">Manage student profiles and enrollment</p>
                </div>
                <button className="btn-primary flex items-center gap-2">
                    <Plus className="w-5 h-5" />
                    Add Student
                </button>
            </div>

            <div className="flex items-center gap-4 bg-white p-4 rounded-xl shadow-sm border border-gray-100">
                <div className="flex-1 flex items-center gap-2 px-1">
                    <Search className="w-5 h-5 text-gray-400" />
                    <input
                        type="text"
                        placeholder="Search students..."
                        className="w-full bg-transparent outline-none text-sm"
                    />
                </div>
                <select className="bg-transparent text-sm font-medium outline-none border-l pl-4">
                    <option>All Grades</option>
                    <option>Grade 10</option>
                    <option>Grade 11</option>
                </select>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                <table className="w-full text-left">
                    <thead className="bg-gray-50 border-b">
                        <tr>
                            <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Name</th>
                            <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Admission</th>
                            <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Class</th>
                            <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Status</th>
                            <th className="px-6 py-4 text-xs font-bold uppercase text-gray-500">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y">
                        {students.map((student) => (
                            <tr key={student.id} className="hover:bg-gray-50 transition-colors">
                                <td className="px-6 py-4">
                                    <div className="flex items-center gap-3">
                                        <div className="w-8 h-8 rounded-full bg-brand-green-light flex items-center justify-center text-brand-green font-bold text-xs">
                                            {student.name.split(' ').map(n => n[0]).join('')}
                                        </div>
                                        <span className="font-medium text-brand-navy">{student.name}</span>
                                    </div>
                                </td>
                                <td className="px-6 py-4 text-sm text-gray-600">{student.admission}</td>
                                <td className="px-6 py-4 text-sm text-gray-600">{student.class}</td>
                                <td className="px-6 py-4">
                                    <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase ${student.status === 'Active' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                                        }`}>
                                        {student.status}
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
