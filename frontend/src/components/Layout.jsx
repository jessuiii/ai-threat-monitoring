import { Shield, LayoutDashboard, Activity, Settings, Bell } from 'lucide-react';

const SidebarItem = ({ icon: Icon, label, active }) => (
    <button
        className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 group
    ${active
                ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 shadow-[0_0_15px_-3px_rgba(6,182,212,0.2)]'
                : 'text-gray-400 hover:text-white hover:bg-white/5'
            }`}
    >
        <Icon className="w-5 h-5" />
        <span className="font-medium text-sm">{label}</span>
        {active && (
            <div className="ml-auto w-1.5 h-1.5 rounded-full bg-cyan-400 shadow-[0_0_8px_rgba(34,211,238,0.8)]" />
        )}
    </button>
);

export default function Layout({ children }) {
    return (
        <div className="min-h-screen bg-dark-bg selection:bg-cyan-500/30 selection:text-white overflow-hidden relative">
            {/* Background Effects */}
            <div className="fixed inset-0 pointer-events-none z-0">
                <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-cyan-500/5 rounded-full blur-[120px]" />
                <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-violet-500/5 rounded-full blur-[120px]" />
            </div>

            {/* Main Content */}
            <main className="relative z-10 p-8 max-w-7xl mx-auto space-y-8">
                {children}
            </main>
        </div>
    );
}
