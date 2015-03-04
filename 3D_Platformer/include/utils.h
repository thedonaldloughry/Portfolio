// DEBUGGING OUTPUT
#ifdef _DEBUG
#define DEBUGVAR(x) do{std::cout << #x << ": " << x << std::endl;}while(0)
#define DEBUGSTR(x) do{std::cout << x << std::endl;}while(0) 
#else
#define DEBUGVAR(x)
#define DEBUGSTR(x)
#endif