
import React from 'react';
import { motion } from 'framer-motion';
import { ShieldAlert, FileSearch, Scale, Info } from 'lucide-react';

const ContractDetails = ({ contract }) => {
    if (!contract) return null;

    const container = {
        hidden: { opacity: 0 },
        show: { opacity: 1, transition: { staggerChildren: 0.2 } }
    };

    const item = {
        hidden: { x: -20, opacity: 0 },
        show: { x: 0, opacity: 1 }
    };

    return (
        <motion.div 
            variants={container}
            initial="hidden"
            animate="show"
            className="space-y-6"
        >
            {/* Executive Summary */}
            <motion.div variants={item} className="bg-white p-6 rounded-2xl shadow-md border-l-8 border-blue-500">
                <div className="flex items-center gap-2 mb-4 text-blue-600">
                    <Info size={20} />
                    <h2 className="text-xl font-bold">Executive Summary</h2>
                </div>
                <p className="text-gray-700 leading-relaxed text-lg italic">
                    {contract.summary}
                </p>
            </motion.div>

            {/* Clauses Grid */}
            <div className="grid grid-cols-1 gap-4">
                <ClauseCard 
                    variant={item} 
                    title="Termination Conditions" 
                    text={contract.termination_clause} 
                    icon={<ShieldAlert className="text-red-500" />} 
                    bgColor="bg-red-50"
                />
                <ClauseCard 
                    variant={item} 
                    title="Confidentiality Obligations" 
                    text={contract.confidentiality_clause} 
                    icon={<FileSearch className="text-purple-500" />} 
                    bgColor="bg-purple-50"
                />
                <ClauseCard 
                    variant={item} 
                    title="Liability Limits" 
                    text={contract.liability_clause} 
                    icon={<Scale className="text-orange-500" />} 
                    bgColor="bg-orange-50"
                />
            </div>
        </motion.div>
    );
};

const ClauseCard = ({ variant, title, text, icon, bgColor }) => (
    <motion.div 
        variants={variant}
        whileHover={{ x: 10 }}
        className={`${bgColor} p-5 rounded-xl border border-gray-100 shadow-sm`}
    >
        <div className="flex items-center gap-3 mb-2 font-bold text-gray-800 uppercase tracking-wide text-sm">
            {icon}
            {title}
        </div>
        <p className="text-gray-600 text-sm whitespace-pre-wrap">
            {text || "No specific clause detected by AI."}
        </p>
    </motion.div>
);

export default ContractDetails;