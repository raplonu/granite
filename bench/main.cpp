#include <iostream>
#include <string>
#include <tuple>
#include <vector>
#include <numeric>
#include <chrono>
#include <algorithm>
#include <benchmark/benchmark.h>


using std::cout;

#define FWD(...) ::std::forward<decltype(__VA_ARGS__)>(__VA_ARGS__)

template<typename Fn>
constexpr auto partialize(Fn fn) {
    return [fn](auto && ... args1) {
        return [fn, args1...](auto && ... args2) {
            return fn(args1..., FWD(args2)...);
        };
    };
}

template<typename It>
auto iterator_predicate(const It last) {
    return [last](const It first) {
        return first != last;
    };
}



struct count_iterator {
    int value;
    struct Value{};

    constexpr Value operator*() const noexcept { return Value{};}
    constexpr count_iterator & operator++() noexcept { ++value; return *this;}
    constexpr bool operator!=(const count_iterator & oci) const noexcept {
        if(BENCHMARK_BUILTIN_EXPECT(value != oci.value, true)) return true;
        return false;
    }
};

struct count_range {
    int size;

    constexpr count_iterator begin() const {
        return count_iterator{0};
    }

    constexpr count_iterator end() const {
        return count_iterator{size};
    }
};






template<typename clock>
struct timer_bench_unit {
    using d_clock = clock;
    using d_time_point = typename d_clock::time_point;
    using d_duration = typename d_clock::duration;
    d_time_point t0;

    void start() noexcept {
        t0 = d_clock::now();
    }

    auto stop() const noexcept {
        return  d_clock::now() - t0;
    }

};

using steady_timer_bench_unit = timer_bench_unit<std::chrono::steady_clock>;

template<typename... Benchs> struct Staked_Bench;

template<typename Bench, typename... Benchs>
struct Staked_Bench<Bench, Benchs...> {
    Bench bench;
    Staked_Bench<Benchs...> o_benchs;

    using result_type = std::tuple<decltype(bench.stop()), decltype(std::declval<Benchs&>().stop())...>;


    Staked_Bench(Bench b, Benchs... bs): bench(b), o_benchs(bs...) {}

    void start() noexcept {
        bench.start();

        o_benchs.start();
    }

    result_type stop() noexcept {
        auto res = o_benchs.stop();

        return std::tuple_cat(std::make_tuple(bench.stop()), std::move(res));
    }
};

template<>
struct Staked_Bench<> {

    using result_type = std::tuple<>;

    constexpr void start() const noexcept {}

    constexpr auto stop() const noexcept {
        return std::make_tuple();
    }
};


template<typename... Benchs>
auto make_staked_bench(Benchs... benchs){
    return Staked_Bench<Benchs...>(benchs...);
}


template<typename It>
struct iterator_consumer_t {
    It output;
    
    template<typename T>
    void operator()(T && data) noexcept {
        *output = FWD(data);
        ++output;
    }
};

template<typename It>
auto iterator_consumer(It output) {
    return iterator_consumer_t<It>{output};
}



template<typename F, typename O, typename E>
auto bench_functor(F f, O output, E executor) {
    return [=] (auto && ... input) mutable {
        executor.start();
        
        f(FWD(input)...);
        
        *output = executor.stop();
        ++output;
    };
}

std::vector<int> fun(int n) {
    std::vector<int> res(n);
    std::iota(std::begin(res), std::end(res), 0);
    return res;
}


template<class Tuple, std::size_t N>
struct TuplePrinter {
    static void print(const Tuple& t) 
    {
        TuplePrinter<Tuple, N-1>::print(t);
        std::cout << ", " << std::get<N-1>(t).count();
    }
};
 
template<class Tuple>
struct TuplePrinter<Tuple, 1> {
    static void print(const Tuple& t) 
    {
        std::cout << std::get<0>(t).count();
    }
};
 
template<class... Args>
void print(const std::tuple<Args...>& t) 
{
    std::cout << "(";
    TuplePrinter<decltype(t), sizeof...(Args)>::print(t);
    std::cout << ")\n";
}

int main()
{
    // Context c;
    //std::vector<int> in {3, 2, 1};
    count_range cr{100};

    auto sb = make_staked_bench(
        steady_timer_bench_unit{},
        steady_timer_bench_unit{},
        steady_timer_bench_unit{},
        steady_timer_bench_unit{},
        steady_timer_bench_unit{},
        steady_timer_bench_unit{},
        steady_timer_bench_unit{},
        steady_timer_bench_unit{},
        steady_timer_bench_unit{},
        steady_timer_bench_unit{},
        steady_timer_bench_unit{},
        steady_timer_bench_unit{},
        steady_timer_bench_unit{},
        steady_timer_bench_unit{});

    std::vector<typename decltype(sb)::result_type> out;

    auto bf = bench_functor(
        [](auto){
            benchmark::DoNotOptimize(fun(100));
        },
        std::back_inserter(out),
        sb
    );

    
    std::for_each(cr.begin(), cr.end(), bf);

    // for (auto _ : cr) {
    //     bf();
    // }

    cout << "\n\n";
    for(auto e : out){
        print(e); //cout << '\n';
    }
    
    std::cout << "ok\n";
}















// struct Context;

// struct context_iterator {
//     const Context & context;
//     int pos;
    
//     const Context & operator*() {
//         return context;
//     }
    
//     context_iterator& operator++() {
//         ++pos;
        
//         return *this;
//     }
    
//     bool operator!=(context_iterator const & oci) const {
//         return pos != oci.pos;
//     }
// };
    

// struct Context {
//     context_iterator begin() const {
//         return context_iterator { *this, 0 };
//     };
    
//     context_iterator end() const {
//         return context_iterator { *this, 100 };
//     };
// };