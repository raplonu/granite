#include <iostream>
#include <string>
#include <tuple>
#include <vector>
#include <chrono>
#include <algorithm>
#include <execution>

using std::cout;

struct Context;

struct context_iterator {
    const Context & context;
    int pos;
    
    const Context & operator*() {
        return context;
    }
    
    context_iterator& operator++() {
        ++pos;
        
        return *this;
    }
    
    bool operator!=(context_iterator const & oci) const {
        return pos != oci.pos;
    }
};
    

struct Context {
    context_iterator begin() const {
        return context_iterator { *this, 0 };
    };
    
    context_iterator end() const {
        return context_iterator { *this, 100 };
    };
};

template<typename It>
auto iterator_predicate(const It last) {
    return [last](const It first) {
        return first != last;
    };
}





template<typename clock>
struct timer_bench_unit {
    using d_clock = clock;
    using d_time_point = typename d_clock::time_point;
    using d_duration = typename d_clock::duration;
    d_time_point t0;

    void start(const Context &) {
        t0 = d_clock::now();
    }

    auto stop(const Context &) const {
        return  d_clock::now() - t0;
    }

};

using steady_timer_bench_unit = timer_bench_unit<std::chrono::steady_clock>;



template<typename It>
struct iterator_consumer_t {
    It output;
    
    template<typename T>
    void operator()(T data) {
        *output = data;
        ++output;
    }
};

template<typename It>
auto iterator_consumer(It output) {
    return iterator_consumer_t<It>{output};
}









/*
template<typename It, typename P, typename C>
auto bench(It input, P pred, C consumer) {
    while(pred(input)) {
        consumer(*input);
        ++input;
    }
    return std::make_tuple( input, consumer );
} 

template<typename InputIt, typename OutputIt>
auto bench(InputIt first, InputIt last, OutputIt first_o) {
    return bench(first, iterator_predicate(last), iterator_consumer(first_o));
}
*/

template<typename F, typename O, typename E>
auto bench_functor(F f, O output, E executor) {
    return [=] (auto & input) mutable {
        //cout << "Iteration : " << input << '\n';
        executor.start(input);
        
        f(input);
        
        *output = executor.stop(input);
        ++output;
    };
}



/*
template<typename InputIterator, typename Predicate, typename Function, typename BenchUnit, typename Consumer>   
auto bench(InputIterator begin, Predicate pred, Function fun, BenchUnit bench_unit, Consumer consumer) {
    while(pred(input)) {
        consumer(*input);   
        ++input;
    }
    return std::make_tuple(begin, consumer);
}
*/

void fun() {
    cout << "call fun";    
}

int main()
{
    Context c;
    //std::vector<int> in {3, 2, 1};
    
    std::vector<std::chrono::steady_clock::duration> out;

    
    std::for_each(std::execution::par, c.begin(), c.end(), bench_functor(
        [](Context const &){fun();},
        std::back_inserter(out),
        steady_timer_bench_unit{}
    ));
    
    /*
    auto bf = bench_functor(
        [](Context const & c)
        {
            fun();
            //also log this :
            c.log();
        },
        std::back_inserter(out),
        steady_timer_bench_unit{}
    );
    
    for(auto const & cr : c)
        bf(cr);
    */
    //example :
    // bench(iter_n(100), fun, bench_units(timer_bench_unit{}), std::back_inserter(out));
    
    // int -> range, 
    // bench(in, fun, bench_units(timer_bench_unit{}), out.end());
    
    // Context c;
    // bench(

    //bench(c.begin(), iterator_predicate(c.end()), );
    

    cout << "\n\n";
    for(auto e : out)
        cout << e.count() << ",";
    

    
    cout << "and\n";
    
    //auto result = 
    //data.stop();
    
    std::cout << "ok\n";
}
