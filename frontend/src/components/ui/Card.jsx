import clsx from 'clsx';
import { twMerge } from 'tailwind-merge';

export const Card = ({ children, className, ...props }) => {
    return (
        <div
            className={twMerge(
                "glass rounded-xl p-6 border-white/5 shadow-xl shadow-black/20",
                className
            )}
            {...props}
        >
            {children}
        </div>
    );
};

export const CardHeader = ({ title, subtitle, className }) => (
    <div className={twMerge("flex flex-col gap-1 mb-6", className)}>
        <h3 className="text-lg font-semibold text-white tracking-wide">{title}</h3>
        {subtitle && <p className="text-sm text-gray-400">{subtitle}</p>}
    </div>
);
