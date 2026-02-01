import { Card } from './ui/Card';

export default function StatCard({ title, value, subtext, icon: Icon, trend }) {
    return (
        <Card className="relative overflow-hidden group">
            <div className="relative z-10">
                <div className="flex items-start justify-between mb-4">
                    <div className="p-2.5 rounded-lg bg-white/5 border border-white/10 text-gray-300 group-hover:text-white group-hover:bg-cyan-500/10 group-hover:border-cyan-500/20 transition-colors">
                        <Icon className="w-5 h-5" />
                    </div>
                    {trend && (
                        <span className={`text-xs font-medium px-2 py-1 rounded-full border ${trend === 'up'
                                ? 'bg-red-500/10 text-red-400 border-red-500/20'
                                : 'bg-green-500/10 text-green-400 border-green-500/20'
                            }`}>
                            {trend === 'up' ? '↑ High' : '↓ Low'}
                        </span>
                    )}
                </div>

                <div className="space-y-1">
                    <p className="text-sm font-medium text-gray-400">{title}</p>
                    <h4 className="text-2xl font-bold text-white tracking-tight">{value}</h4>
                </div>
            </div>

            <div className="absolute right-0 top-0 w-32 h-32 bg-gradient-to-br from-white/5 to-transparent rounded-full blur-2xl -mr-16 -mt-16 group-hover:from-cyan-500/10 transition-colors duration-500" />
        </Card>
    );
}
