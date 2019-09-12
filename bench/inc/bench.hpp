#ifndef GRANITE_BENCH_HPP
#define GRANITE_BENCH_HPP
#pragma once

#include <chrono>

namespace granite {
    namespace bench {

        // TODO : Add donotoptimise
        // TODO : Add fast loop
        using d_clock = std::chrono::steady_clock;
        using d_time_point = typename d_clock::time_point;
        using d_duration = typename d_clock::duration;

        template<typename Executor>
        struct scoped_executor {
            Executor & executor;

            scoped_executor(Executor & executor) : executor(executor) {
                executor.start();
            }

            ~scoped_executor() {
                
            }
        }

        template<typename... Executor>
        struct multi_executor {
            std::tuple<Executor...> data;
        };

        template<typename It>
        auto iterator_predicate(const It last) {
            return [last](const It first) {
                return first != last;
            }
        }

        template<typename It>
        auto iterator_consumer(It output) {
            return [output] (auto data) mutable {
                *output = data;
                ++output;
            }
        }



        template<typename It, typename P, typename C>
        auto bench(It input, P pred, C consumer) {
            while(pred(input)) {
                consume(*input);
                ++input;
            }
            return std::make_tuple( input, consume );
        } 

        template<typename InputIt, typename OutputIt>
        auto bench(InputIt first, InputIt last, OutputIt first_o) {
            return bench(first, iterator_predicate(last), iterator_consumer(first_o));
        } 

        

        struct steady_timer {
            d_time_point start;

            steady_timer() {}
            
            void start() {
                start = d_clock::now();
            }

            auto stop() const {
                return  d_clock::now() - start;
            }

        };



        struct State {
            int iter_limit = 100;
            d_duration duration_limit = 5s;

            bool expired(int iter, d_duration d) {
                return iter == iter_limit || d > duration_limit;
            }
        };

        struct bench_iterator {
            using clock_type = d_clock;
            State state;
            int iteration_nb;
            steady_timer timer;

            bench_iterator(State state):
                state(state), iteration_nb(0),
                timer()
            {
                timer.start();
            }

            State& operator*() {
                return state;
            }

            bench_iterator& operator++() noexcept {
                ++iteration_nb;
                return *this;
            }

            bool end() {
                return state.expired(iteration_nb, timer.stop());
            }
        };

        bool bench_predicate(const bench_iterator& bi) {  
            return bi.end();
        }


        template<>
        struct fun {
            

            void operator()(State& state) {
                auto scoped = scoped_bench(generator, );

                under_fun();


            }
        }




        template<typename G>
        struct scoped_symetric_generator_t {
            using data_type = decltype(std::declval<G&>()());
            
            G generator;
            




        };



        template<typename G, typename It>
        struct bench_guard_t {
            G g;
            It it;
            const auto start = g();

            ~bench_guard_t() {
                const auto stop = g();

                *it = stop - start;
            } 
        };


        template<typename >
        struct BenchIt {


            auto operator()(auto input) {
                auto bg = bench_guard(g, out_it);
                f();

            }
        };
        

        

    }
}

#endif //GRANITE_BENCH_HPP