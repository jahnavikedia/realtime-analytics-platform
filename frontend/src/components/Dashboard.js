import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import CountUp from 'react-countup';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { fetchDashboardSummary, fetchCategoryBreakdown } from '../services/api';

const Dashboard = () => {
  const [summary, setSummary] = useState(null);
  const [categories, setCategories] = useState(null);
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(new Date());
  const [countdown, setCountdown] = useState(30);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [summaryData, categoryData] = await Promise.all([
        fetchDashboardSummary(),
        fetchCategoryBreakdown()
      ]);
      
      setSummary(summaryData.data);
      setCategories(categoryData.data);
      setLastUpdated(new Date());
      setCountdown(30);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      setCountdown(prev => prev > 0 ? prev - 1 : 30);
    }, 1000);
    return () => clearInterval(timer);
  }, [lastUpdated]);

  if (loading && !summary) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-white"></div>
      </div>
    );
  }

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  const categoryData = categories ? Object.entries(categories.categories).map(([name, value]) => ({
    name,
    value
  })) : [];

  const eventDistribution = summary ? [
    { name: 'Views', value: summary.metrics.product_view },
    { name: 'Cart Adds', value: summary.metrics.add_to_cart },
    { name: 'Purchases', value: summary.metrics.purchase },
    { name: 'Removals', value: summary.metrics.remove_from_cart }
  ] : [];

  return (
    <div className="min-h-screen p-8">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-7xl mx-auto"
      >
        {/* Header */}
        <div className="text-center mb-12">
          <motion.h1
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            className="text-5xl font-bold text-white mb-4"
          >
            📊 Real-Time Analytics Dashboard
          </motion.h1>
          <p className="text-white/80 text-lg">
            Live insights from {summary?.metrics.product_view || 0} total events
          </p>
          <div className="mt-4 flex items-center justify-center gap-4">
            <span className="text-white/60 text-sm">
              Last updated: {lastUpdated.toLocaleTimeString()}
            </span>
            <button
              onClick={fetchData}
              className="px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg text-white text-sm backdrop-blur-sm transition-all"
            >
              🔄 Refresh Now
            </button>
            <span className="text-white/60 text-sm">
              Auto-refresh in {countdown}s
            </span>
          </div>
        </div>

        {/* Metric Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <MetricCard
            title="Product Views"
            value={summary?.metrics.product_view || 0}
            icon="👁️"
            color="from-blue-500 to-cyan-500"
          />
          <MetricCard
            title="Cart Additions"
            value={summary?.metrics.add_to_cart || 0}
            icon="🛒"
            color="from-green-500 to-emerald-500"
          />
          <MetricCard
            title="Purchases"
            value={summary?.metrics.purchase || 0}
            icon="💰"
            color="from-purple-500 to-pink-500"
          />
          <MetricCard
            title="Conversion Rate"
            value={summary?.conversion_rate || 0}
            icon="📈"
            color="from-orange-500 to-red-500"
            suffix="%"
          />
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Category Breakdown */}
          <ChartCard title="📊 Category Performance">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={categoryData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="name" stroke="#fff" />
                <YAxis stroke="#fff" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    border: 'none',
                    borderRadius: '8px',
                    color: '#fff'
                  }}
                />
                <Bar dataKey="value" fill="#8884d8" radius={[8, 8, 0, 0]}>
                  {categoryData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>

          {/* Event Distribution */}
          <ChartCard title="🎯 Event Distribution">
            <ResponsiveContainer width="100%" height={300}>
             <PieChart>
  <Pie
    data={eventDistribution}
    cx="50%"
    cy="50%"
    outerRadius={100}
    fill="#8884d8"
    dataKey="value"
    label={({ name, value }) => `${name}: ${value}`}
  >
    {eventDistribution.map((entry, index) => (
      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
    ))}
  </Pie>
  <Tooltip
    contentStyle={{
      backgroundColor: 'rgba(255,255,255,0.95)',
      border: 'none',
      borderRadius: '8px',
      color: '#000',
      padding: '8px 12px'
    }}
  />
</PieChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        {/* Business Insights */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <InsightCard
            title="Cart Abandonment Rate"
            value={summary?.cart_abandonment_rate || 0}
            suffix="%"
            description="Percentage of users who add to cart but don't purchase"
            status={summary?.cart_abandonment_rate > 70 ? 'high' : summary?.cart_abandonment_rate > 50 ? 'medium' : 'low'}
          />
          <InsightCard
            title="Conversion Funnel"
            value={`${summary?.metrics.product_view || 0} → ${summary?.metrics.add_to_cart || 0} → ${summary?.metrics.purchase || 0}`}
            description="Views → Cart → Purchases"
            status="neutral"
          />
        </div>
      </motion.div>
    </div>
  );
};

const MetricCard = ({ title, value, icon, color, suffix = '' }) => (
  <motion.div
    whileHover={{ scale: 1.05, y: -5 }}
    className={`bg-gradient-to-br ${color} p-6 rounded-2xl shadow-2xl backdrop-blur-sm`}
  >
    <div className="flex items-center justify-between mb-4">
      <span className="text-4xl">{icon}</span>
      <div className="text-white/80 text-sm font-medium">{title}</div>
    </div>
    <div className="text-4xl font-bold text-white">
      <CountUp end={value} duration={2} decimals={suffix === '%' ? 2 : 0} />
      {suffix}
    </div>
  </motion.div>
);

const ChartCard = ({ title, children }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="bg-white/10 backdrop-blur-md p-6 rounded-2xl shadow-2xl border border-white/20"
  >
    <h3 className="text-xl font-bold text-white mb-4">{title}</h3>
    {children}
  </motion.div>
);

const InsightCard = ({ title, value, suffix = '', description, status }) => {
  const statusColors = {
    high: 'text-red-400',
    medium: 'text-yellow-400',
    low: 'text-green-400',
    neutral: 'text-blue-400'
  };

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className="bg-white/10 backdrop-blur-md p-6 rounded-2xl shadow-2xl border border-white/20"
    >
      <h3 className="text-lg font-semibold text-white mb-2">{title}</h3>
      <div className={`text-3xl font-bold ${statusColors[status]} mb-2`}>
        {typeof value === 'number' ? (
          <>
            <CountUp end={value} duration={2} decimals={suffix === '%' ? 2 : 0} />
            {suffix}
          </>
        ) : (
          value
        )}
      </div>
      <p className="text-white/60 text-sm">{description}</p>
    </motion.div>
  );
};

export default Dashboard;
