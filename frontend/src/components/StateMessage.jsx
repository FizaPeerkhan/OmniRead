export default function StateMessage({ type = 'info', title, children }) {
  const styles = {
    info: 'border-indigo-100 bg-indigo-50 text-indigo-900',
    error: 'border-red-100 bg-red-50 text-red-900',
    warning: 'border-amber-100 bg-amber-50 text-amber-900',
  };
  return (
    <div className={`rounded-2xl border p-5 ${styles[type] || styles.info}`} role={type === 'error' ? 'alert' : 'status'}>
      <p className="font-semibold">{title}</p>
      <div className="mt-1 text-sm opacity-85">{children}</div>
    </div>
  );
}
