
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, FileText, Loader2 } from 'lucide-react';
import axios from 'axios';

const FileUploader = ({ onUploadSuccess }) => {
    const [isUploading, setIsUploading] = useState(false);

    const handleFileChange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        setIsUploading(true);
        try {
            const response = await axios.post('http://localhost:5000/api/upload', formData);
            onUploadSuccess(response.data);
        } catch (error) {
            alert("Upload failed. Ensure Flask is running.");
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="w-full max-w-2xl mx-auto p-8 mb-8 bg-white rounded-2xl shadow-xl border-2 border-dashed border-blue-200"
        >
            <div className="flex flex-col items-center">
                <AnimatePresence mode="wait">
                    {isUploading ? (
                        <motion.div 
                            key="loading"
                            initial={{ scale: 0.8, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.8, opacity: 0 }}
                            className="flex flex-col items-center py-10"
                        >
                            <motion.div 
                                animate={{ rotate: 360 }}
                                transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
                            >
                                <Loader2 size={48} className="text-blue-500" />
                            </motion.div>
                            <p className="mt-4 text-blue-600 font-semibold animate-pulse">
                                Groq AI is analyzing your contract...
                            </p>
                        </motion.div>
                    ) : (
                        <motion.label 
                            key="input"
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                            className="flex flex-col items-center cursor-pointer py-10"
                        >
                            <div className="p-4 bg-blue-50 rounded-full mb-4 text-blue-600">
                                <Upload size={32} />
                            </div>
                            <span className="text-xl font-bold text-gray-700">Upload New Contract</span>
                            <span className="text-sm text-gray-400 mt-2">PDF files from CUAD dataset</span>
                            <input type="file" className="hidden" onChange={handleFileChange} accept=".pdf" />
                        </motion.label>
                    )}
                </AnimatePresence>
            </div>
        </motion.div>
    );
};

export default FileUploader;